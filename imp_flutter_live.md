# Flutter Live Assistant — Implementation Guide

Hướng dẫn kết nối Flutter app với **TRIAM Live Assistant** WebSocket endpoint để thực hiện hội thoại giọng nói real-time.

---

## Architecture

```
Flutter App
  │
  ├── 🎙️ Microphone (PCM 16kHz, 16-bit, mono)
  │         │  raw bytes
  │         ▼
  │   WebSocket send → ws://<server>/api/v1/ws/live-assistant/{book_id}
  │
  └── 🔊 Speaker ← WebSocket receive (PCM 24kHz, 16-bit, mono)
```

**Audio format contracts:**
| Direction | Format | Sample Rate | Channels | Bit Depth |
|---|---|---|---|---|
| Client → Server (mic) | PCM raw | 16,000 Hz | 1 (mono) | 16-bit |
| Server → Client (AI voice) | PCM raw | 24,000 Hz | 1 (mono) | 16-bit |

---

## 1. Dependencies — `pubspec.yaml`

```yaml
dependencies:
  flutter:
    sdk: flutter

  # WebSocket
  web_socket_channel: ^2.4.0

  # Microphone recording → PCM stream
  record: ^5.1.2 # streams raw PCM bytes

  # PCM audio playback
  just_audio: ^0.9.40 # or flutter_pcm_sound (see note below)
  flutter_pcm_sound: ^1.1.0 # plays raw PCM without WAV header

permissions:
  # Android: AndroidManifest.xml
  # iOS: Info.plist
```

> **Note on playback:** `flutter_pcm_sound` plays raw PCM directly.
> `just_audio` requires a WAV header wrapper — see Section 4.

---

## 2. Add Permissions

### Android — `android/app/src/main/AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.INTERNET"/>
```

### iOS — `ios/Runner/Info.plist`

```xml
<key>NSMicrophoneUsageDescription</key>
<string>TRIAM cần microphone để bạn có thể nói chuyện với AI.</string>
```

---

## 3. Live Assistant Service — `lib/services/live_assistant_service.dart`

```dart
import 'dart:async';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:record/record.dart';

class LiveAssistantService {
  // ── Config ──────────────────────────────────────────────────────────────
  static const String _baseUrl = 'ws://YOUR_SERVER_IP:8000'; // 🔧 Change this
  static const int _sendSampleRate = 16000;   // mic → server
  static const int _receiveSampleRate = 24000; // server → speaker

  // ── State ────────────────────────────────────────────────────────────────
  WebSocketChannel? _channel;
  final AudioRecorder _recorder = AudioRecorder();
  StreamSubscription? _micSubscription;

  // Expose incoming audio to UI
  final StreamController<Uint8List> _audioController =
      StreamController<Uint8List>.broadcast();
  Stream<Uint8List> get audioStream => _audioController.stream;

  bool get isConnected => _channel != null;

  // ── Connect ──────────────────────────────────────────────────────────────
  Future<void> connect(String bookId) async {
    final uri = Uri.parse('$_baseUrl/api/v1/ws/live-assistant/$bookId');
    _channel = WebSocketChannel.connect(uri);

    // Wait for the connection to be established
    await _channel!.ready;
    print('✅ WebSocket connected');

    // Listen for incoming audio from Gemini
    _channel!.stream.listen(
      (data) {
        if (data is List<int>) {
          _audioController.add(Uint8List.fromList(data));
        } else if (data is Uint8List) {
          _audioController.add(data);
        }
      },
      onError: (e) => print('❌ WS error: $e'),
      onDone: () {
        print('📴 WebSocket closed');
        _channel = null;
      },
    );
  }

  // ── Start Microphone Streaming ───────────────────────────────────────────
  Future<void> startMicrophone() async {
    // Check permission
    final hasPermission = await _recorder.hasPermission();
    if (!hasPermission) throw Exception('Microphone permission denied');

    // Stream raw PCM from microphone → WebSocket
    final micStream = await _recorder.startStream(
      const RecordConfig(
        encoder: AudioEncoder.pcm16bits, // raw PCM, no container
        sampleRate: _sendSampleRate,
        numChannels: 1,
      ),
    );

    _micSubscription = micStream.listen((chunk) {
      if (_channel != null) {
        // Send raw PCM bytes directly
        _channel!.sink.add(Uint8List.fromList(chunk));
      }
    });

    print('🎙️ Microphone streaming started');
  }

  // ── Stop Microphone ──────────────────────────────────────────────────────
  Future<void> stopMicrophone() async {
    await _micSubscription?.cancel();
    _micSubscription = null;
    await _recorder.stop();
    print('🎙️ Microphone stopped');
  }

  // ── Disconnect ───────────────────────────────────────────────────────────
  Future<void> disconnect() async {
    await stopMicrophone();
    await _channel?.sink.close();
    _channel = null;
    print('📴 Disconnected');
  }

  void dispose() {
    disconnect();
    _audioController.close();
  }
}
```

---

## 4. PCM Audio Playback — `lib/services/audio_player_service.dart`

### Option A — `flutter_pcm_sound` (recommended, no header needed)

```dart
import 'dart:typed_data';
import 'package:flutter_pcm_sound/flutter_pcm_sound.dart';

class PcmPlayerService {
  static const int _sampleRate = 24000; // Must match server output rate
  bool _initialized = false;

  Future<void> initialize() async {
    await FlutterPcmSound.setup(
      sampleRate: _sampleRate,
      channelCount: 1,
    );
    _initialized = true;
  }

  Future<void> play(Uint8List pcmBytes) async {
    if (!_initialized) await initialize();
    // Convert raw bytes to Int16 samples
    final samples = pcmBytes.buffer.asInt16List();
    await FlutterPcmSound.feed(PcmArrayInt16(bytes: samples.buffer.asUint8List()));
  }

  Future<void> stop() async {
    await FlutterPcmSound.clear();
  }
}
```

### Option B — `just_audio` (wrap PCM in WAV header)

```dart
import 'dart:typed_data';
import 'package:just_audio/just_audio.dart';

class WavPlayerService {
  final AudioPlayer _player = AudioPlayer();
  static const int _sampleRate = 24000;

  /// Wraps raw PCM bytes in a WAV header so just_audio can decode it
  Uint8List _wrapInWav(Uint8List pcm) {
    final dataSize = pcm.length;
    final fileSize = 36 + dataSize;
    final header = ByteData(44)
      ..setUint32(0, 0x52494646, Endian.big)   // "RIFF"
      ..setUint32(4, fileSize, Endian.little)
      ..setUint32(8, 0x57415645, Endian.big)   // "WAVE"
      ..setUint32(12, 0x666d7420, Endian.big)  // "fmt "
      ..setUint32(16, 16, Endian.little)        // chunk size
      ..setUint16(20, 1, Endian.little)         // PCM format
      ..setUint16(22, 1, Endian.little)         // 1 channel
      ..setUint32(24, _sampleRate, Endian.little)
      ..setUint32(28, _sampleRate * 2, Endian.little) // byte rate
      ..setUint16(32, 2, Endian.little)         // block align
      ..setUint16(34, 16, Endian.little)        // bits per sample
      ..setUint32(36, 0x64617461, Endian.big)  // "data"
      ..setUint32(40, dataSize, Endian.little);
    return Uint8List.fromList(header.buffer.asUint8List() + pcm);
  }

  Future<void> play(Uint8List pcmBytes) async {
    final wav = _wrapInWav(pcmBytes);
    final source = AudioSource.uri(
      Uri.dataFromBytes(wav, mimeType: 'audio/wav'),
    );
    await _player.setAudioSource(source);
    await _player.play();
  }

  void dispose() => _player.dispose();
}
```

---

## 5. UI Widget — `lib/widgets/live_assistant_button.dart`

```dart
import 'dart:async';
import 'package:flutter/material.dart';
import '../services/live_assistant_service.dart';
import '../services/audio_player_service.dart'; // choose Option A or B

class LiveAssistantButton extends StatefulWidget {
  final String bookId;
  const LiveAssistantButton({super.key, required this.bookId});

  @override
  State<LiveAssistantButton> createState() => _LiveAssistantButtonState();
}

class _LiveAssistantButtonState extends State<LiveAssistantButton>
    with SingleTickerProviderStateMixin {
  final _service = LiveAssistantService();
  final _player = PcmPlayerService(); // or WavPlayerService()
  StreamSubscription? _audioSub;

  bool _isListening = false;
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    )..repeat(reverse: true);
  }

  Future<void> _toggleListening() async {
    if (_isListening) {
      await _service.stopMicrophone();
      await _service.disconnect();
      await _audioSub?.cancel();
      setState(() => _isListening = false);
    } else {
      try {
        await _service.connect(widget.bookId);
        await _player.initialize();

        // Play incoming audio chunks
        _audioSub = _service.audioStream.listen((pcmBytes) async {
          await _player.play(pcmBytes);
        });

        await _service.startMicrophone();
        setState(() => _isListening = true);
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Lỗi kết nối: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        final scale = _isListening
            ? 1.0 + (_pulseController.value * 0.15)
            : 1.0;
        return Transform.scale(
          scale: scale,
          child: FloatingActionButton.large(
            onPressed: _toggleListening,
            backgroundColor: _isListening ? Colors.red : Colors.deepPurple,
            child: Icon(
              _isListening ? Icons.mic : Icons.mic_none,
              size: 40,
              color: Colors.white,
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _service.dispose();
    super.dispose();
  }
}
```

---

## 6. Usage in a Page

```dart
import 'package:flutter/material.dart';
import 'widgets/live_assistant_button.dart';

class BookDetailPage extends StatelessWidget {
  final String bookId;
  const BookDetailPage({super.key, required this.bookId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('TRIAM Assistant')),
      body: const Center(
        child: Text('Nhấn nút micro để bắt đầu hỏi AI về nội dung sách'),
      ),
      floatingActionButton: LiveAssistantButton(bookId: bookId),
    );
  }
}
```

---

## 7. Troubleshooting

| Problem                     | Cause                                 | Fix                                            |
| --------------------------- | ------------------------------------- | ---------------------------------------------- |
| `WebSocketChannelException` | Wrong server URL/port                 | Check `_baseUrl` in `LiveAssistantService`     |
| No audio received (0 bytes) | Sent silence → Gemini doesn't respond | Send real mic audio, not silence               |
| Choppy playback             | Chunks too small                      | Buffer 2–4 chunks before playing               |
| `RECORD_AUDIO` crash        | Permission not requested              | Use `permission_handler` to request at runtime |
| iOS mic not working         | `Info.plist` key missing              | Add `NSMicrophoneUsageDescription`             |
| Echo / feedback             | Mic picks up speaker                  | Use headphones during testing                  |

---

## 8. Production Checklist

- [ ] Replace `ws://` with `wss://` (TLS) in production
- [ ] Add JWT auth token as WebSocket query param: `?token=<jwt>`
- [ ] Handle `WebSocketChannelException` with auto-reconnect logic
- [ ] Add noise suppression via `RecordConfig.noiseCancel = true`
- [ ] Test on both Android (API 26+) and iOS (14+)
