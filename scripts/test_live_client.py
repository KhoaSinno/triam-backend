"""
Test client for the TRIAM Live Assistant WebSocket endpoint.

Usage:
    python test_live_client.py

This script:
  1. Connects to ws://127.0.0.1:8000/api/v1/ws/live-assistant/test-book-123
  2. Sends 3 seconds of silence (PCM 16-bit, 16kHz, mono) as audio input
  3. Listens for any audio response bytes from Gemini
  4. Disconnects cleanly after 5 seconds

Make sure the server is running first:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""
import asyncio
import struct

import websockets

WS_URI = "ws://127.0.0.1:8000/api/v1/ws/live-assistant/test-book-123"

# PCM audio constants — must match server expectations
SEND_SAMPLE_RATE = 16000   # Hz
CHANNELS = 1
SAMPLE_WIDTH = 2           # 16-bit = 2 bytes
CHUNK_DURATION_MS = 100    # Send 100ms chunks
CHUNK_SAMPLES = SEND_SAMPLE_RATE * CHUNK_DURATION_MS // 1000
CHUNK_BYTES = CHUNK_SAMPLES * CHANNELS * SAMPLE_WIDTH

# Total duration to send audio
SEND_DURATION_SECONDS = 3
TOTAL_CHUNKS = (SEND_DURATION_SECONDS * 1000) // CHUNK_DURATION_MS


def make_silence_chunk() -> bytes:
    """Generate one chunk of silent PCM audio (all zeros)."""
    return struct.pack(f"<{CHUNK_SAMPLES}h", *([0] * CHUNK_SAMPLES))


async def test_live_client():
    print(f"🔌 Đang kết nối tới: {WS_URI}")
    try:
        async with websockets.connect(WS_URI, ping_interval=None) as ws:
            print("✅ Kết nối WebSocket thành công!")
            bytes_received = 0

            async def send_audio():
                """Send silence PCM chunks to simulate microphone input."""
                silence = make_silence_chunk()
                for i in range(TOTAL_CHUNKS):
                    await ws.send(silence)
                    await asyncio.sleep(CHUNK_DURATION_MS / 1000)
                print(f"📤 Đã gửi {TOTAL_CHUNKS} chunks ({SEND_DURATION_SECONDS}s audio)")

            async def receive_audio():
                """Receive and measure audio response from Gemini."""
                nonlocal bytes_received
                try:
                    # Listen for 5 seconds total
                    deadline = asyncio.get_event_loop().time() + 5
                    while asyncio.get_event_loop().time() < deadline:
                        try:
                            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                            if isinstance(msg, bytes):
                                bytes_received += len(msg)
                                print(f"🔊 Nhận được audio chunk: {len(msg):,} bytes "
                                      f"(tổng: {bytes_received:,} bytes)")
                            else:
                                print(f"📝 Text từ server: {msg}")
                        except asyncio.TimeoutError:
                            continue
                except websockets.exceptions.ConnectionClosedOK:
                    pass

            await asyncio.gather(send_audio(), receive_audio())
            print(f"\n✅ Test hoàn thành! Tổng audio nhận: {bytes_received:,} bytes")

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Lỗi HTTP status: {e.status_code}")
    except ConnectionRefusedError:
        print("❌ Server không chạy. Hãy khởi động server trước:")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"❌ Lỗi: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(test_live_client())
