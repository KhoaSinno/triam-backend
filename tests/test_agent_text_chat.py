"""
Test: Agent Text Chat + RAG Call
================================
Script này sẽ:
1. Lấy LiveKit token từ backend API
2. Kết nối vào LiveKit Room với tư cách là một "user" ảo
3. Gửi câu hỏi qua Data Channel (lk.chat) cho Agent
4. Lắng nghe phản hồi từ Agent (text/data) trong 20 giây
5. In kết quả ra console để xác nhận RAG hoạt động

Cách chạy:
  uv run python tests/test_agent_text_chat.py
"""

import asyncio
import json
import sys

import aiohttp
from livekit import api, rtc

# ─── CẤU HÌNH ──────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"
TEST_QUESTION = "Tên tác giả và nội dung quyển sách này là gì?"
WAIT_TIMEOUT_SECONDS = 25  # Thời gian chờ tối đa cho phản hồi của agent
# ───────────────────────────────────────────────────────────────────────────


async def get_livekit_token(session: aiohttp.ClientSession) -> str:
    """Lấy token từ backend API để kết nối vào LiveKit Room."""
    url = f"{BASE_URL}/live-token/{MOCK_BOOK_ID}"
    print(f"\n[1/4] 🔑 Lấy token từ: {url}")
    async with session.get(url) as resp:
        if resp.status != 200:
            body = await resp.text()
            raise RuntimeError(f"❌ API trả về {resp.status}: {body}")
        data = await resp.json()
        token = data.get("token")
        if not token:
            raise RuntimeError(f"❌ Không tìm thấy 'token' trong response: {data}")
        print(f"   ✅ Token nhận được (đầu): {token[:40]}...")
        return token


async def main() -> None:
    print("=" * 60)
    print("   TRIAM Agent - Text Chat & RAG Integration Test")
    print("=" * 60)

    received_responses: list[str] = []
    agent_joined = asyncio.Event()
    agent_replied = asyncio.Event()

    # ─── Bước 1: Lấy token ─────────────────────────────────────────────────
    async with aiohttp.ClientSession() as http_session:
        token = await get_livekit_token(http_session)

    # ─── Bước 2: Kết nối vào LiveKit Room ──────────────────────────────────
    room = rtc.Room()

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"\n[2/4] 👤 Participant tham gia: {participant.identity} ({participant.kind})")
        # Agent thường có kind = PARTICIPANT_KIND_AGENT
        if "agent" in participant.identity.lower() or participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            print("   ✅ AGENT đã kết nối vào phòng!")
            agent_joined.set()

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        try:
            text = packet.data.decode("utf-8")
            sender = packet.participant.identity if packet.participant else "unknown"
            print(f"\n[4/4] 💬 Nhận phản hồi từ [{sender}] qua '{packet.topic}':")
            print(f"   ─────────────────────────────────────────")
            print(f"   {text}")
            print(f"   ─────────────────────────────────────────")
            received_responses.append(text)
            agent_replied.set()
        except Exception as e:
            print(f"   ⚠️  Không decode được data: {e}")

    print(f"\n[2/4] 🔌 Kết nối vào LiveKit Room: {MOCK_BOOK_ID[:20]}...")
    await room.connect(LIVEKIT_URL, token)
    print(f"   ✅ Đã vào phòng! Participant local: '{room.local_participant.identity}'")
    print(f"   📋 Số participant hiện tại: {len(room.remote_participants)}")

    # Kiểm tra xem Agent đã có trong phòng chưa (có thể đã join trước)
    for identity, p in room.remote_participants.items():
        print(f"   👥 Có sẵn: {identity} (kind={p.kind})")
        if "agent" in identity.lower() or p.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            print("   ✅ AGENT đang sẵn sàng trong phòng!")
            agent_joined.set()

    # Chờ Agent join (nếu chưa vào)
    if not agent_joined.is_set():
        print("\n   ⏳ Chờ Agent tham gia phòng (tối đa 15s)...")
        try:
            await asyncio.wait_for(agent_joined.wait(), timeout=15.0)
        except asyncio.TimeoutError:
            print("   ⚠️  Agent chưa join trong 15s. Vẫn tiếp tục gửi tin nhắn...")

    # ─── Bước 3: Gửi câu hỏi qua lk.chat ──────────────────────────────────
    print(f"\n[3/4] 📤 Gửi câu hỏi qua Data Channel 'lk.chat':")
    print(f"   Câu hỏi: \"{TEST_QUESTION}\"")
    await asyncio.sleep(1.5)  # Cho agent thời gian khởi động xong

    await room.local_participant.publish_data(
        TEST_QUESTION.encode("utf-8"),
        reliable=True,
        topic="lk.chat",
    )
    print("   ✅ Đã gửi! Đang chờ Agent xử lý và trả lời...")

    # ─── Bước 4: Chờ phản hồi ──────────────────────────────────────────────
    print(f"\n   ⏳ Chờ phản hồi tối đa {WAIT_TIMEOUT_SECONDS}s...")
    try:
        await asyncio.wait_for(agent_replied.wait(), timeout=WAIT_TIMEOUT_SECONDS)
        print("\n✅ ========== KẾT QUẢ KIỂM TRA ==========")
        print(f"   Tổng số phản hồi nhận được: {len(received_responses)}")
        for i, r in enumerate(received_responses, 1):
            print(f"\n   📨 Phản hồi #{i}:\n   {r}")
        print("\n✅ Agent TEXT CHAT hoạt động bình thường!")
        print("   Kiểm tra worker.log để xác nhận RAG tool có được gọi không.")
    except asyncio.TimeoutError:
        print(f"\n❌ TIMEOUT sau {WAIT_TIMEOUT_SECONDS}s - Không nhận được phản hồi.")
        print("   Gợi ý kiểm tra:")
        print("   1. Kiểm tra worker.log xem agent có lỗi không")
        print("   2. Kiểm tra agent đã join phòng chưa")
        print("   3. Server start.sh có đang chạy không?")

    await room.disconnect()
    print("\n🔌 Đã ngắt kết nối. Test kết thúc.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Test bị ngắt bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        sys.exit(1)
