Future<void> \_startLiveKit() async {
// Stop audio when start livekit
if (\_bookPlayer.state == PlayerState.playing) {
\_bookPlayer.pause();
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
