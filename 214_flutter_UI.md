import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:audio_session/audio_session.dart' as audio_session;
import 'package:http/http.dart' as http;
import 'package:livekit_client/livekit_client.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';

enum _AssistantState {
  idle,
  resolvingHost,
  fetchingToken,
  connectingRoom,
  connected,
  disconnecting,
  error,
}

const String mockBookId = "87543419-c71f-4d7e-9e0d-036b4ab9b81e";
const String strLiveKitUrl = "wss://tri-am-bmdl413w.livekit.cloud";

// ---------------------------------------------------------
// MODEL
// ---------------------------------------------------------

class Book {
  final String title;
  final String author;
  final int totalChapters;
  final String status;
  final DateTime createdAt;
  final String errorMessage;
  final String userId;
  final String fileUrl;

  Book({
    this.title = '',
    this.author = '',
    this.totalChapters = 0,
    this.status = '',
    DateTime? createdAt,
    this.errorMessage = '',
    this.userId = '',
    this.fileUrl = '',
  }) : createdAt = createdAt ?? DateTime(2000);

  factory Book.fromJson(Map<String, dynamic> json) {
    return Book(
      title: json['title'] ?? '',
      author: json['author'] ?? '',
      totalChapters: json['total_chapters'] ?? 0,
      status: json['status'] ?? '',
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at']) ?? DateTime(2000)
          : DateTime(2000),
      errorMessage: json['error_message'] ?? '',
      userId: json['user_id'] ?? '',
      fileUrl: json['file_url'] ?? '',
    );
  }
}

// ---------------------------------------------------------
// REPOSITORY (Xử lý API)
// ---------------------------------------------------------
class TestLabRepository {
  static const String fallbackBackendHost = '127.0.0.1';
  static String backendHost = const String.fromEnvironment(
    'TRIAM_BACKEND_HOST',
    defaultValue: '',
  );
  static const int backendPort = 8000;

  static String get resolvedBackendHost =>
      backendHost.isNotEmpty ? backendHost : fallbackBackendHost;

  String get baseUrl => 'http://$resolvedBackendHost:$backendPort/api/v1';

  Future<Map<String, dynamic>> getBookDetails({
    String bookId = mockBookId,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/books/$bookId/details'),
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load book details");
    }
  }

  Future<Map<String, dynamic>> getBookById({String bookId = mockBookId}) async {
    final response = await http.get(Uri.parse('$baseUrl/books/$bookId'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load book");
    }
  }
}

class LiveKitEndpointResolver {
  static const String fallbackUrl = strLiveKitUrl;

  static String get liveKitUrl => const String.fromEnvironment(
    'TRIAM_LIVEKIT_URL',
    defaultValue: fallbackUrl,
  );
}

class _LiveKitFixedTokenSource implements TokenSourceFixed {
  final TokenSourceResponse _response;

  _LiveKitFixedTokenSource(this._response);

  @override
  Future<TokenSourceResponse> fetch() async => _response;
}

// ---------------------------------------------------------
// UI SCREEN (Test Lab)
// ---------------------------------------------------------
class ListenAudioTestLabScreen extends ConsumerStatefulWidget {
  const ListenAudioTestLabScreen({super.key});

  @override
  ConsumerState<ListenAudioTestLabScreen> createState() =>
      _AudioTestLabScreenState();
}

class _AudioTestLabScreenState extends ConsumerState<ListenAudioTestLabScreen> {
  final TestLabRepository _repo = TestLabRepository();
  final AudioPlayer _bookPlayer = AudioPlayer();
  final _audioRecorder = AudioRecorder();

  // State File & API
  String _statusMessage = "Sẵn sàng...";
  List<dynamic> _chaptersOutline = [];
  Book _book = Book();

  // State Assistant (LiveKit)
  bool _isAssisting = false;
  _AssistantState _assistantState = _AssistantState.idle;
  Future<void>? _assistantOp;
  DateTime? _lastToggleAt;
  DateTime? _lastStoppedAt;
  int _toggleActionId = 0;
  Timer? _roomGraceTimer;
  Timer? _pollingTimer;

  Session? _session;

  Room? get _room => _session?.room;

  int? _playChapIdx;
  int? _playSegIdx;
  Future<void>? _backendHostInitFuture;

  static const Duration _toggleDebounce = Duration(milliseconds: 400);
  static const Duration _reopenCooldown = Duration(milliseconds: 900);
  static const List<int> _connectRetryDelaysSec = [1, 2, 4];
  static const Duration _roomGraceDuration = Duration(seconds: 35);

  bool get _assistantBusy =>
      _assistantState == _AssistantState.resolvingHost ||
      _assistantState == _AssistantState.fetchingToken ||
      _assistantState == _AssistantState.connectingRoom ||
      _assistantState == _AssistantState.disconnecting;

  @override
  void initState() {
    super.initState();

    _initialFetch();

    // Lắng nghe sự kiện AudioPlayer phát xong 1 segment để nhảy sang segment tiếp theo
    _bookPlayer.onPlayerComplete.listen((event) {
      if (_playChapIdx != null && _playSegIdx != null) {
        _playSegIdx = _playSegIdx! + 1;
        _playNextSegmentInChapter();
      }
    });
  }

  // --- ⬆️ LOGIC UPLOAD & GENERATE PLAN ---

  Future<void> _ensureBackendHostReady() async {
    if (TestLabRepository.backendHost.isNotEmpty) return;

    if (mounted) {
      setState(() {
        _statusMessage = '🌐 Đang xác định backend host...';
      });
    }

    final future = (_backendHostInitFuture ??= _autoSelectBackendHost());
    await future.timeout(
      const Duration(seconds: 3),
      onTimeout: () {
        TestLabRepository.backendHost = TestLabRepository.fallbackBackendHost;
        debugPrint(
          '[NET] Resolve timeout, dùng fallback: '
          '${TestLabRepository.fallbackBackendHost}',
        );
      },
    );

    if (TestLabRepository.backendHost.isEmpty) {
      TestLabRepository.backendHost = TestLabRepository.fallbackBackendHost;
    }

    if (mounted) {
      setState(() {
        _statusMessage =
            '🌐 Backend host: ${TestLabRepository.resolvedBackendHost}';
      });
    }
  }

  Future<void> _initialFetch() async {
    await _ensureBackendHostReady();
    try {
      setState(() => _statusMessage = "⏳ Đang tải dữ liệu sách...");
      final data = await _repo.getBookDetails(bookId: mockBookId);
      final bookJson = await _repo.getBookById(bookId: mockBookId);

      if (mounted) {
        setState(() {
          _chaptersOutline = data['chapters'] ?? [];
          _book = Book.fromJson(bookJson);
          _statusMessage = "✅ Đã sẵn sàng thảo luận.";
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _statusMessage = "❌ Lỗi tải sách: $e");
      }
    }
  }

  Future<void> _autoSelectBackendHost() async {
    // Ưu tiên host được truyền từ --dart-define=TRIAM_BACKEND_HOST=...
    if (TestLabRepository.backendHost.isNotEmpty) return;

    final baseCandidates = <String>[
      TestLabRepository.fallbackBackendHost,
      '10.0.2.2', // Android emulator -> host machine
      '127.0.0.1',
    ];

    final subnetCandidates = await _buildSubnetCandidates();
    final allCandidates = <String>{...baseCandidates, ...subnetCandidates};

    for (final host in allCandidates) {
      if (await _isBackendReachable(host)) {
        TestLabRepository.backendHost = host;
        debugPrint('[NET] Backend host auto-selected: $host');
        if (mounted) {
          setState(() {
            _statusMessage = '🌐 Backend host: $host';
          });
        }
        return;
      }
    }

    debugPrint(
      '[NET] Không tìm thấy backend khả dụng. Dùng fallback: '
      '${TestLabRepository.fallbackBackendHost}',
    );
  }

  Future<List<String>> _buildSubnetCandidates() async {
    try {
      final interfaces = await NetworkInterface.list(
        type: InternetAddressType.IPv4,
        includeLoopback: false,
      );

      final results = <String>[];
      for (final iface in interfaces) {
        for (final addr in iface.addresses) {
          final ip = addr.address;
          if (!_isPrivateIpv4(ip)) continue;

          // Giữ danh sách nhẹ để tránh treo khi user bấm mic lần đầu.
          results.add(ip);

          final octets = ip.split('.');
          if (octets.length == 4) {
            final prefix = '${octets[0]}.${octets[1]}.${octets[2]}';
            results.add('$prefix.1');
          }
        }
      }
      return results;
    } catch (e) {
      debugPrint('[NET] Không đọc được interface mạng: $e');
      return [];
    }
  }

  bool _isPrivateIpv4(String ip) {
    if (ip.startsWith('10.')) return true;
    if (ip.startsWith('192.168.')) return true;
    if (ip.startsWith('172.')) {
      final parts = ip.split('.');
      if (parts.length >= 2) {
        final second = int.tryParse(parts[1]) ?? -1;
        return second >= 16 && second <= 31;
      }
    }
    return false;
  }

  Future<bool> _isBackendReachable(String host) async {
    try {
      final docsUri = Uri.parse(
        'http://$host:${TestLabRepository.backendPort}/docs',
      );
      final response = await http
          .get(docsUri)
          .timeout(const Duration(milliseconds: 350));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  // --- 🎧 LOGIC PHÁT SÁCH LIÊN TỤC ---
  Future<void> _playChapter(int chapterIndex) async {
    await _stopLiveKitAssistant();

    setState(() {
      _playChapIdx = chapterIndex;
      _playSegIdx = 0;
    });
    await _playNextSegmentInChapter();
  }

  Future<void> _playNextSegmentInChapter() async {
    if (_playChapIdx == null || _playSegIdx == null) return;

    final chap = _chaptersOutline[_playChapIdx!];
    final segs = chap['chapter_segments'] as List? ?? [];

    if (_playSegIdx! < segs.length) {
      final url = segs[_playSegIdx!]['audio_url'];
      if (url != null) {
        try {
          setState(
            () => _statusMessage =
                "🔊 Đang phát: ${chap['title']} (Phần ${_playSegIdx! + 1}/${segs.length})",
          );
          await _bookPlayer.stop();
          await _bookPlayer.play(UrlSource(url));
        } catch (e) {
          setState(() => _statusMessage = "❌ Lỗi Play: $e");
        }
      } else {
        // Bỏ qua đoạn hỏng url, skip tới đoạn sau
        _playSegIdx = _playSegIdx! + 1;
        _playNextSegmentInChapter();
      }
    } else {
      // Đã hát hết dòng segment hiện có. Kiểm tra xem chapter còn gen tiếp không
      if (chap['status'] != 'READY') {
        setState(
          () => _statusMessage =
              "⏳ Đang chờ AI gen tiếp đoạn tiếp theo của chương...",
        );
        // Hệ thống Polling 3s sẽ tự kiểm tra và gọi lại _playNextSegmentInChapter khi có dòng mới
      } else {
        setState(() => _statusMessage = "✅ Đã phát xong ${chap['title']}");
        _playChapIdx = null; // Trả về null để ngưng phát
      }
    }
  }

  // --- 🎤 LOGIC TRỢ LÝ AI (LIVEKIT ONLY) ---

  void _setAssistantState(_AssistantState next) {
    if (_assistantState == next) return;
    if (!mounted) {
      _assistantState = next;
      return;
    }
    setState(() {
      _assistantState = next;
    });
  }

  Future<void> _runAssistantOp(Future<void> Function() op) async {
    final running = _assistantOp;
    if (running != null) {
      await running;
      return;
    }

    final future = op();
    _assistantOp = future;
    try {
      await future;
    } finally {
      if (identical(_assistantOp, future)) {
        _assistantOp = null;
      }
    }
  }

  Future<void> _disconnectAndDisposeRoom({required String reason}) async {
    _roomGraceTimer?.cancel();
    _roomGraceTimer = null;

    final currentSession = _session;
    _session = null;
    if (currentSession == null) return;

    final currentRoom = currentSession.room;

    debugPrint('[LiveKit] Room disconnect start ($reason)');
    try {
      currentRoom.unregisterByteStreamHandler('lk.agent.session');
    } catch (_) {}

    try {
      await currentRoom.localParticipant?.setMicrophoneEnabled(false);
    } catch (e) {
      debugPrint('[LiveKit] Mic disable before disconnect failed: $e');
    }
    try {
      await currentSession.end();
      debugPrint('[LiveKit] Room disconnected ($reason)');
    } catch (e) {
      debugPrint('[LiveKit] Room disconnect error ($reason): $e');
    }

    try {
      await currentSession.dispose();
    } catch (e) {
      debugPrint('[LiveKit] Session dispose failed ($reason): $e');
    }

    try {
      final session = await audio_session.AudioSession.instance;
      await session.setActive(false);
    } catch (e) {
      debugPrint('[LiveKit] Audio session deactivate failed: $e');
    }
  }

  // LOG: Đăng ký handler để nhận byte stream từ Agent gửi về (ví dụ luồng dữ liệu audio giả định), đọc và log ra console.
  void _attachAgentSessionHandler(Room room) {
    try {
      room.registerByteStreamHandler('lk.agent.session', (
        ByteStreamReader reader,
        String participantIdentity,
      ) {
        unawaited(_consumeAgentSessionStream(reader, participantIdentity));
      });
      debugPrint(
        '[LiveKit] Registered byte stream handler for lk.agent.session',
      );
    } catch (_) {
      // Handler đã được đăng ký trước đó trên cùng room instance.
    }
  }

  // LOG: Đọc toàn bộ stream từ Agent, tính tổng bytes và log ra để demo luồng dữ liệu audio giả định.
  Future<void> _consumeAgentSessionStream(
    ByteStreamReader reader,
    String participantIdentity,
  ) async {
    try {
      final chunks = await reader.readAll();
      int totalBytes = 0;
      for (final chunk in chunks) {
        totalBytes += chunk.length;
      }
      debugPrint(
        '[LiveKit] lk.agent.session stream consumed: '
        'from=$participantIdentity chunks=${chunks.length} bytes=$totalBytes',
      );
    } catch (e) {
      debugPrint('[LiveKit] lk.agent.session stream read error: $e');
    }
  }

  Future<void> _toggleAssistant() async {
    final actionId = ++_toggleActionId;
    final now = DateTime.now();
    if (_lastToggleAt != null &&
        now.difference(_lastToggleAt!) < _toggleDebounce) {
      debugPrint('[LiveKit] Toggle ignored (debounce) action=$actionId');
      return;
    }
    _lastToggleAt = now;

    if (_assistantBusy) {
      debugPrint(
        '[LiveKit] Toggle ignored (busy=$_assistantState) action=$actionId',
      );
      return;
    }

    debugPrint('[LiveKit] Toggle action=$actionId state=$_assistantState');
    if (_assistantState == _AssistantState.connected || _isAssisting) {
      await _stopLiveKitAssistant();
      if (mounted) {
        setState(() => _statusMessage = "Đã dừng trợ lý AI.");
      }
      return;
    }

    await _startLiveKit();
  }

  Future<void> _startLiveKit() async {
    // Stop audio when start livekit
    if (_bookPlayer.state == PlayerState.playing) {
      _bookPlayer.pause();
    }

    await _runAssistantOp(() async {
      _roomGraceTimer?.cancel();
      _roomGraceTimer = null;

      // Nếu user bật lại nhanh trong cửa sổ grace, ưu tiên resume mic trên room cũ.
      final warmRoom = _room;
      if (warmRoom != null) {
        try {
          await warmRoom.localParticipant?.setMicrophoneEnabled(true);

          try {
            await Hardware.instance.setSpeakerphoneOn(true);
          } catch (_) {}

          debugPrint('[LiveKit] Warm resume success (reuse existing room)');
          _setAssistantState(_AssistantState.connected);
          if (mounted) {
            setState(() {
              _isAssisting = true;
              _statusMessage = '🎤 Đã nối lại trợ lý ngay lập tức';
            });
          }
          return;
        } catch (e) {
          debugPrint(
            '[LiveKit] Warm resume failed, fallback hard reconnect: $e',
          );
          await _disconnectAndDisposeRoom(reason: 'warm-resume-failed');
        }
      }

      if (_lastStoppedAt != null) {
        final elapsed = DateTime.now().difference(_lastStoppedAt!);
        if (elapsed < _reopenCooldown) {
          final waitFor = _reopenCooldown - elapsed;
          debugPrint(
            '[LiveKit] Cooldown before reopen: ${waitFor.inMilliseconds}ms',
          );
          await Future<void>.delayed(waitFor);
        }
      }

      _setAssistantState(_AssistantState.resolvingHost);
      await _ensureBackendHostReady();

      // Check permission
      if (!await _audioRecorder.hasPermission()) {
        _setAssistantState(_AssistantState.error);
        if (mounted) {
          setState(() => _statusMessage = "❌ Chưa cấp quyền Micro.");
        }
        return;
      }

      // Stop audio player
      await _bookPlayer.stop();

      try {
        // Cấu hình audio session để tối ưu cho trường hợp thoại, giúp giảm độ trễ và ưu tiên thiết bị âm thanh phù hợp.
        // Hỗ trợ mặc định ra Loa ngoài (Speaker), giảm tiếng vọng.
        final session = await audio_session.AudioSession.instance;
        await session.configure(
          audio_session.AudioSessionConfiguration(
            avAudioSessionCategory:
                audio_session.AVAudioSessionCategory.playAndRecord,
            avAudioSessionCategoryOptions:
                audio_session.AVAudioSessionCategoryOptions.allowBluetooth |
                audio_session.AVAudioSessionCategoryOptions.defaultToSpeaker,
            avAudioSessionMode: audio_session.AVAudioSessionMode.voiceChat,
            avAudioSessionRouteSharingPolicy:
                audio_session.AVAudioSessionRouteSharingPolicy.defaultPolicy,
            avAudioSessionSetActiveOptions:
                audio_session.AVAudioSessionSetActiveOptions.none,
            androidAudioAttributes: const audio_session.AndroidAudioAttributes(
              contentType: audio_session.AndroidAudioContentType.speech,
              usage: audio_session.AndroidAudioUsage.voiceCommunication,
            ),
            androidAudioFocusGainType:
                audio_session.AndroidAudioFocusGainType.gain,
            androidWillPauseWhenDucked: true,
          ),
        );
        await session.setActive(true);

        _setAssistantState(_AssistantState.fetchingToken);
        if (mounted) {
          setState(() {
            _statusMessage = '🔑 Đang lấy token LiveKit...';
          });
        }
        // Call API Get token LiveKit from BE, pass BookId to BE join room with current book context
        final tokenUri = Uri.parse('${_repo.baseUrl}/live-token/$mockBookId');
        debugPrint('[LiveKit] Token request start: $tokenUri');
        final response = await http.get(tokenUri);
        debugPrint(
          '[LiveKit] Token request end: status=${response.statusCode}',
        );

        if (response.statusCode != 200) {
          _setAssistantState(_AssistantState.error);
          if (mounted) {
            setState(() {
              _statusMessage =
                  '❌ Không lấy được token LiveKit (${response.statusCode})';
            });
          }
          return;
        }

        final token = jsonDecode(response.body)['token'] as String?;
        if (token == null || token.isEmpty) {
          _setAssistantState(_AssistantState.error);
          if (mounted) {
            setState(
              () => _statusMessage = '❌ Token LiveKit rỗng/không hợp lệ',
            );
          }
          return;
        }

        // Decode token to get data session
        final liveKitUrl = LiveKitEndpointResolver.liveKitUrl;
        final tokenResponse = TokenSourceResponse(
          serverUrl: liveKitUrl,
          participantToken: token,
        );
        debugPrint(
          '[LiveKit] Token dispatches agent: ${tokenResponse.dispatchesAgent()}',
        );

        await _disconnectAndDisposeRoom(reason: 'before new connect');

        for (int i = 0; i < _connectRetryDelaysSec.length; i++) {
          final attempt = i + 1;
          _setAssistantState(_AssistantState.connectingRoom);
          if (mounted) {
            setState(() {
              _statusMessage = '🔌 Kết nối LiveKit (lần $attempt/3)...';
            });
          }

          final sessionOptions = SessionOptions(
            preConnectAudio: false,
            agentConnectTimeout: const Duration(seconds: 15),
          );

          final candidateSession = Session.fromFixedTokenSource(
            _LiveKitFixedTokenSource(tokenResponse),
            options: sessionOptions,
          );
          try {
            _attachAgentSessionHandler(candidateSession.room);
            debugPrint(
              '[LiveKit] Connecting Room & Chờ Agent join (attempt=$attempt)... url=$liveKitUrl',
            );

            await candidateSession.start();
            debugPrint(
              '[LiveKit] Connect & Agent join THÀNH CÔNG: attempt=$attempt',
            );

            // Bật Microphone ngay sau khi Room + Agent đã sẵn sàng
            try {
              await candidateSession.room.localParticipant
                  ?.setMicrophoneEnabled(true);

              try {
                await Hardware.instance.setSpeakerphoneOn(true);
              } catch (_) {}

              debugPrint(
                '[LiveKit] 🎤 Microphone đã được bật, AI có thể nghe bạn!',
              );
            } catch (e) {
              debugPrint('[LiveKit] ❌ Không thể bật microphone: $e');
            }

            _session = candidateSession;
            _setAssistantState(_AssistantState.connected);
            if (mounted) {
              setState(() {
                _isAssisting = true;
                _statusMessage = "🎤 Đang thảo luận cùng AI...";
              });
            }
            return;
          } catch (e) {
            debugPrint(
              '[LiveKit] Connect Room hoặc Chờ Agent Timeout/Lỗi (attempt=$attempt): $e',
            );
            try {
              await candidateSession.end();
            } catch (_) {}
            try {
              await candidateSession.dispose();
            } catch (_) {}

            if (attempt >= _connectRetryDelaysSec.length) {
              _setAssistantState(_AssistantState.error);
              if (mounted) {
                setState(() {
                  _isAssisting = false;
                  _statusMessage = '❌ Không thể kết nối. Vui lòng thử lại sau.';
                });
              }
              return;
            }

            final waitSec = _connectRetryDelaysSec[i];
            await Future<void>.delayed(Duration(seconds: waitSec));
          }
        }
      } catch (e) {
        debugPrint("Lỗi LiveKit: $e");
        _setAssistantState(_AssistantState.error);
        if (mounted) {
          setState(() {
            _isAssisting = false;
            _statusMessage = "❌ Không thể kết nối LiveKit";
          });
        }
        await _disconnectAndDisposeRoom(reason: 'start failed');
      }
    });
  }

  Future<void> _stopLiveKitAssistant() async {
    await _runAssistantOp(() async {
      _setAssistantState(_AssistantState.disconnecting);
      if (mounted) {
        setState(() {
          _statusMessage = '⏹️ Đang tắt trợ lý...';
        });
      }

      // Soft-stop: tắt mic ngay để user thấy đã dừng, giữ room 1 khoảng ngắn để mở lại tức thì.
      final currentRoom = _room;
      if (currentRoom != null) {
        try {
          await currentRoom.localParticipant?.setMicrophoneEnabled(false);
          debugPrint('[LiveKit] Mic disabled (soft-stop)');
        } catch (e) {
          debugPrint('[LiveKit] Soft-stop mic disable failed: $e');
        }

        _roomGraceTimer?.cancel();
        _roomGraceTimer = Timer(_roomGraceDuration, () {
          unawaited(_disconnectAndDisposeRoom(reason: 'grace-timeout'));
        });
      }

      _lastStoppedAt = DateTime.now();
      _setAssistantState(_AssistantState.idle);
      if (mounted) {
        setState(() {
          _isAssisting = false;
          _statusMessage = '⏸️ Đã dừng trợ lý (giữ kết nối tạm thời)';
        });
      }
    });
  }

  @override
  void dispose() {
    _isAssisting = false;
    _roomGraceTimer?.cancel();
    _setAssistantState(_AssistantState.disconnecting);
    unawaited(_disconnectAndDisposeRoom(reason: 'dispose'));
    _pollingTimer?.cancel();
    _bookPlayer.dispose();
    _audioRecorder.dispose();
    super.dispose();
  }

  // --- 🎨 BUILD UI ---

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Test Lab Flow")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // STATUS BANNER
            Container(
              padding: const EdgeInsets.all(12),
              color: Colors.blue.withOpacity(0.1),
              child: Text(
                _statusMessage,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 16),

            // Live preview book from book URL
            _buildPdfPreview(),
            const SizedBox(height: 16),
            // Play list audio UI
            _buildAudioPlayer(),
            const SizedBox(height: 16),

            // fetch OUTLINE LIST WITH SEGMENTS
            const Text(
              "Outline sách",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),

            // Fetch here UI:
            // - toggle chapter
            // - playing status chapter
            // - segment content joined
            _buildOutline(),

            const SizedBox(height: 300), // Khoảng trống cho FAB
          ],
        ),
      ),
      floatingActionButton: _buildAssistantFab(),
    );
  }

  // PDF preview UI
  Widget _buildPdfPreview() {
    if (_book.fileUrl.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              "Xem trước sách",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            // TIP: Thêm nút xem toàn màn hình để UX chuyên nghiệp hơn
            IconButton(
              icon: const Icon(Icons.fullscreen),
              onPressed: () => _showFullScreenPdf(context, _book.fileUrl),
            ),
          ],
        ),
        const SizedBox(height: 10),
        // FIX: Bọc trong GestureDetector để chiếm quyền scroll
        SizedBox(
          height: 400,
          child: GestureDetector(
            onVerticalDragUpdate:
                (
                  details,
                ) {}, // Chặn cử chỉ vuốt dọc không truyền lên SingleChildScrollView
            child: SfPdfViewer.network(
              _book.fileUrl,
              canShowScrollHead: false,
              // Tối ưu cho mobile preview
              enableDoubleTapZooming: true,
            ),
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  void _showFullScreenPdf(BuildContext context, String url) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => Scaffold(
          appBar: AppBar(title: const Text("Đọc sách")),
          body: SfPdfViewer.network(url),
        ),
      ),
    );
  }

  // Audio player UI
  Widget _buildAudioPlayer() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          "Trình phát Audio",
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        StreamBuilder<PlayerState>(
          stream: _bookPlayer.onPlayerStateChanged,
          builder: (context, snapshot) {
            final playerState = snapshot.data ?? _bookPlayer.state;
            final isPlaying = playerState == PlayerState.playing;

            return Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16.0,
                  vertical: 16.0,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    // Nút Stop
                    IconButton(
                      icon: const Icon(Icons.stop_rounded),
                      iconSize: 32,
                      color: playerState == PlayerState.stopped
                          ? Colors.grey.shade400
                          : Colors.redAccent,
                      onPressed: playerState == PlayerState.stopped
                          ? null
                          : () {
                              _bookPlayer.stop();
                              setState(() => _playChapIdx = null);
                            },
                    ),

                    // Nút Play / Pause to ở giữa
                    CircleAvatar(
                      radius: 36,
                      backgroundColor: isPlaying
                          ? Colors.orangeAccent
                          : Colors.blueAccent,
                      child: IconButton(
                        icon: Icon(
                          isPlaying
                              ? Icons.pause_rounded
                              : Icons.play_arrow_rounded,
                        ),
                        iconSize: 42,
                        color: Colors.white,
                        onPressed: () {
                          if (isPlaying) {
                            _bookPlayer.pause();
                          } else {
                            if (playerState == PlayerState.paused) {
                              _bookPlayer.resume();
                            } else if (_chaptersOutline.isNotEmpty) {
                              // Phát tiếp chương đang dở hoặc chương đầu tiên
                              _playChapter(_playChapIdx ?? 0);
                            }
                          }
                        },
                      ),
                    ),

                    // Nút Skip Next (Chuyển sang segment/chương tiếp theo)
                    IconButton(
                      icon: const Icon(Icons.skip_next_rounded),
                      iconSize: 32,
                      color: _playChapIdx == null
                          ? Colors.grey.shade400
                          : Colors.blueGrey,
                      onPressed: _playChapIdx == null
                          ? null
                          : () {
                              if (_chaptersOutline.isNotEmpty) {
                                _playNextSegmentInChapter();
                              }
                            },
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  // Outline
  // - toggle chapter
  // - playing status chapter
  // - segment content joined
  Widget _buildOutline() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 10),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _chaptersOutline.length,
          itemBuilder: (context, index) {
            final chap = _chaptersOutline[index];
            List segments = List.from(chap['chapter_segments'] ?? []);
            segments.sort(
              (a, b) => (a['segment_index'] as int? ?? 0).compareTo(
                b['segment_index'] as int? ?? 0,
              ),
            );
            bool isPlayingThisChap = _playChapIdx == index;

            return Card(
              color: isPlayingThisChap
                  ? const Color.fromARGB(255, 41, 45, 42)
                  : null,
              margin: const EdgeInsets.only(bottom: 8.0),
              child: ExpansionTile(
                leading: CircleAvatar(
                  backgroundColor: isPlayingThisChap
                      ? Colors.green
                      : Colors.blue,
                  child: Icon(
                    isPlayingThisChap ? Icons.graphic_eq : Icons.book,
                    color: Colors.white,
                  ),
                ),
                title: Text(chap['title'] ?? 'Chương ${index + 1}'),
                subtitle: Text(
                  chap['review_text'] ?? 'Chưa có nội dung review',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                trailing: IconButton(
                  icon: Icon(
                    isPlayingThisChap
                        ? Icons.stop_circle
                        : Icons.play_circle_fill,
                    size: 32,
                    color: isPlayingThisChap ? Colors.red : Colors.green,
                  ),
                  onPressed: () {
                    if (isPlayingThisChap) {
                      _bookPlayer.stop();
                      setState(() => _playChapIdx = null);
                    } else {
                      _playChapter(index);
                    }
                  },
                ),
                children: segments.isEmpty
                    ? [
                        const Padding(
                          padding: EdgeInsets.all(16.0),
                          child: Text(
                            "Chưa có nội dung segments hoặc đang xử lý...",
                            style: TextStyle(color: Colors.grey),
                          ),
                        ),
                      ]
                    : segments.map((seg) {
                        bool isPlayingThisSeg =
                            isPlayingThisChap &&
                            _playSegIdx == segments.indexOf(seg);
                        return Container(
                          color: isPlayingThisSeg
                              ? const Color.fromARGB(255, 64, 60, 31)
                              : null,
                          child: ListTile(
                            contentPadding: const EdgeInsets.symmetric(
                              horizontal: 40,
                              vertical: 4,
                            ),
                            title: Text(
                              seg['text_content'] ?? 'Đang hiển thị audio...',
                              style: const TextStyle(fontSize: 14),
                              textAlign: TextAlign.justify,
                            ),
                          ),
                        );
                      }).toList(),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildAssistantFab() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 70.0),
      child: FloatingActionButton.large(
        onPressed: _assistantBusy ? null : _toggleAssistant,
        backgroundColor: _assistantBusy
            ? Colors.grey
            : (_isAssisting ? Colors.red : Colors.blue),
        child: Icon(
          _assistantBusy
              ? Icons.hourglass_top
              : (_isAssisting ? Icons.mic_off : Icons.mic),
          color: Colors.white,
          size: 36,
        ),
      ),
    );
  }
}
