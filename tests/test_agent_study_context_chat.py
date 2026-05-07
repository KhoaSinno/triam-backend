import asyncio
import aiohttp
import sys
from livekit import api, rtc

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"
TEST_QUESTION = "Tóm tắt ngắn gọn giúp tôi quyển sách này nói về phương pháp học tập nào? Tên tác giả là gì, có mấy chương"
TITLE_CONTEXT = "ppm 1"

async def main() -> None:
    print("=" * 60)
    print("   KIỂM THỬ: Agent nạp Study Context và Lưu Database")
    print("=" * 60)

    async with aiohttp.ClientSession() as session:
        # 1. Tạo Context
        print("\n[1/6] 📦 Đang tạo Study Context...")
        async with session.post(f"{BASE_URL}/study-contexts", json={"title": "Test Context Phương Pháp Trí Nhớ"}) as r:
            if r.status != 200:
                print(f"❌ Lỗi tạo Context: {await r.text()}")
                return
            ctx = await r.json()
            context_id = ctx["id"]
            print(f"   ✅ Tạo thành công Context ID: {context_id}")

        # 2. Add Document
        print(f"\n[2/6] 📚 Gắn sách {MOCK_BOOK_ID} vào Context...")
        async with session.post(f"{BASE_URL}/study-contexts/{context_id}/documents", json={"book_id": MOCK_BOOK_ID}) as r:
            if r.status != 200:
                print(f"   ⚠️ Warning: Không thể link book (có thể sách không tồn tại): {await r.text()}")
            else:
                print("   ✅ Link thành công sách vào ngữ cảnh.")

        # 3. Tạo Thread
        print("\n[3/6] 💬 Đang tạo Chat Thread...")
        async with session.post(f"{BASE_URL}/study-contexts/{context_id}/threads", json={"title": TITLE_CONTEXT}) as r:
            thread = await r.json()
            thread_id = thread["id"]
            print(f"   ✅ Tạo thành công Thread ID: {thread_id}")

        # 4. Lấy Token LiveKit
        print(f"\n[4/6] 🔑 Lấy LiveKit Token cho Thread...")
        async with session.get(f"{BASE_URL}/live-token/thread/{thread_id}") as r:
            token_data = await r.json()
            token = token_data["token"]
            print(f"   ✅ Nhận token LiveKit thành công.")

    # 5. Kết nối LiveKit
    print("\n[5/6] 🔌 Kết nối vào phòng LiveKit và gọi Agent...")
    room = rtc.Room()
    
    agent_joined = asyncio.Event()
    agent_replied = asyncio.Event()
    greeting_received = asyncio.Event()
    answer_received = asyncio.Event()

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        if "agent" in participant.identity.lower() or participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            print("   ✅ AGENT đã vào phòng!")
            agent_joined.set()

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        text = packet.data.decode("utf-8")
        if packet.participant and "agent" in packet.participant.identity.lower():
            if not greeting_received.is_set():
                print(f"\n   👋 Agent Greeting: {text}")
                greeting_received.set()
            else:
                print(f"\n   💬 Nhận câu trả lời từ Agent [{packet.participant.identity}]:\n   {text}\n")
                answer_received.set()

    await room.connect(LIVEKIT_URL, token)
    
    # Kiểm tra xem agent có đang trong phòng không
    for identity, p in room.remote_participants.items():
        if "agent" in identity.lower() or p.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            print("   ✅ AGENT đang chực sẵn trong phòng!")
            agent_joined.set()

    # Chờ Agent gửi câu chào (Greeting) để đảm bảo Agent đã khởi động xong hoàn toàn
    print("   ⏳ Chờ Agent khởi động (Worker xử lý metadata) và gửi câu chào...")
    try:
        await asyncio.wait_for(greeting_received.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        print("   ❌ Quá thời gian chờ Agent khởi động!")
        await room.disconnect()
        return

    print(f"   📤 Gửi câu hỏi cho Agent: '{TEST_QUESTION}'")
    await room.local_participant.publish_data(
        TEST_QUESTION.encode("utf-8"),
        reliable=True,
        topic="lk.chat",
    )
    
    print("   ⏳ Chờ Agent suy nghĩ và Query RAG...")
    try:
        await asyncio.wait_for(answer_received.wait(), timeout=45.0)
    except asyncio.TimeoutError:
        print("   ❌ Quá thời gian. Không nhận được câu trả lời.")

    print("   ⏳ Chờ thêm 8 giây để Agent hoàn tất TTS Audio và kích hoạt event lưu DB...")
    await asyncio.sleep(8)

    await room.disconnect()
    
    # Đợi 2 giây cho DB kịp commit
    await asyncio.sleep(2)
    
    # 6. Kiểm tra Database
    print("\n[6/6] 🗄️ Đọc Database để xác nhận tin nhắn đã được lưu (Persisted History)...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/threads/{thread_id}/messages") as r:
            if r.status != 200:
                print(f"   ❌ Lỗi lấy lịch sử DB: {await r.text()}")
            else:
                msgs = await r.json()
                print(f"   ✅ TÌM THẤY {len(msgs)} TIN NHẮN TRONG DATABASE:")
                for m in msgs:
                    role = "USER" if m["is_user"] else "AGENT"
                    # Rút gọn tin nhắn nếu quá dài
                    txt = m["text"]
                    short_txt = txt if len(txt) < 80 else txt[:80] + "..."
                    print(f"      [{m['timestamp'][11:19]}] {role}: {short_txt}")
                    
                if len(msgs) >= 2:
                    print("\n🎉 THÀNH CÔNG RỰC RỠ! Agent đã tự động lưu History vào đúng luồng kiến trúc Study Context!")
                else:
                    print("\n⚠️ Có vẻ tin nhắn chưa được lưu đủ (chờ 1 xíu kiểm tra lại worker.log).")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)
