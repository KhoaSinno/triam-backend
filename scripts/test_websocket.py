"""
Test script để kiểm tra WebSocket endpoint Live Assistant
"""
import asyncio

import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8000/api/v1/ws/live-assistant/test-book-123"

    try:
        print(f"🔌 Đang kết nối tới: {uri}")
        async with websockets.connect(uri) as websocket:
            print("✅ Kết nối WebSocket thành công!")
            print(f"📡 WebSocket state: {websocket.state}")
            print(f"🔗 Connected to: {websocket.remote_address}")

            # Giữ kết nối mở một chút để xem log
            await asyncio.sleep(2)

            print("✅ Test hoàn thành!")

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Lỗi status code: {e}")
    except ConnectionRefusedError:
        print("❌ Server không chạy hoặc từ chối kết nối")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
