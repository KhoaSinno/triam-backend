"""
Kiểm thử tích hợp: Chức năng Chat Text-Only với Toggle Web Search

Bao gồm 2 test case:
  - Test A: Toggle TẮT → Naive RAG (mặc định, chỉ tìm trong sách)
  - Test B: Toggle BẬT → Agentic Loop (LLM tự quyết định tìm web nếu cần)
"""
import asyncio
import json
import sys

import aiohttp
from livekit import rtc

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"

# Test A: Câu hỏi trong sách (Naive RAG nên trả lời được)
QUESTION_IN_BOOK = "Tóm tắt ngắn gọn phương pháp ghi nhớ trong cuốn sách này."

# Test B: Câu hỏi ngoài sách tổng quát (verify toggle ON works)
QUESTION_OUTSIDE_BOOK = "Hôm nay ngày mấy? Cho tôi biết giá vàng sjc và doji Việt Nam hôm nay"

# Test C: Danh sách câu hỏi thực tế để verify web search đang chạy thật
# Mỗi câu đặc biệt ở chỗ: chỉ có web search mới trả lời được đúng
WEB_SEARCH_VERIFY_QUESTIONS = [
    "Tỷ giá USD/VND hôm nay là bao nhiêu? Cho tôi biết giá mua và giá bán tại Vietcombank.",
    "Giá Bitcoin (BTC) và Ethereum (ETH) hiện tại là bao nhiêu USD?",
    "Có tin tức nổi bật gì ở Việt Nam trong 24 giờ qua không? Tóm tắt ngắn gọn.",
]

TITLE_CONTEXT = "Test Toggle Web Search"


# ---------------------------------------------------------------------------
# Hàm tiện ích: Setup Study Context + Thread + Token
# ---------------------------------------------------------------------------
async def setup_session() -> tuple[str, str]:
    """Tạo Study Context, link sách, tạo Thread, lấy LiveKit Token.

    Returns:
        (thread_id, livekit_token)
    """
    async with aiohttp.ClientSession() as http:
        r = await http.post(f"{BASE_URL}/study-contexts", json={"title": TITLE_CONTEXT})
        ctx = await r.json()
        context_id = ctx["id"]

        await http.post(
            f"{BASE_URL}/study-contexts/{context_id}/documents",
            json={"book_id": MOCK_BOOK_ID},
        )

        r = await http.post(
            f"{BASE_URL}/study-contexts/{context_id}/threads",
            json={"title": TITLE_CONTEXT},
        )
        thread = await r.json()
        thread_id = thread["id"]

        r = await http.get(f"{BASE_URL}/live-token/thread/{thread_id}")
        token_data = await r.json()
        return thread_id, token_data["token"]


# ---------------------------------------------------------------------------
# Hàm tiện ích: Kết nối LiveKit Room, đợi Agent online
# ---------------------------------------------------------------------------
async def connect_room(token: str) -> tuple[rtc.Room, asyncio.Event, asyncio.Event, asyncio.Event]:
    """Kết nối room, trả về (room, greeting_received, chat_reply_received, transcript_reply_received)."""
    room = rtc.Room()
    greeting_received = asyncio.Event()
    chat_reply_received = asyncio.Event()
    transcript_reply_received = asyncio.Event()

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        if (
            "agent" in participant.identity.lower()
            or participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT
        ):
            pass  # Agent tham gia phòng (không cần event riêng, dùng greeting làm mốc)

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        topic = packet.topic
        if not packet.participant or "agent" not in packet.participant.identity.lower():
            return
        try:
            text = packet.data.decode("utf-8")
        except Exception:
            return

        if topic == "lk.chat":
            if not greeting_received.is_set():
                print(f"   👋 [lk.chat] Agent Greeting: {text[:120]}")
                greeting_received.set()
            else:
                # In FULL response (không cắt) để user tự đánh giá độ chính xác
                print(f"   💬 [lk.chat] AI phản hồi ({len(text)} ký tự):")
                print(f"{text}")
                print()
                chat_reply_received.set()

        elif topic == "lk.transcript":
            try:
                data = json.loads(text)
                if data.get("role") == "assistant" and data.get("type") == "transcript":
                    if greeting_received.is_set():
                        transcript_reply_received.set()
            except Exception:
                pass

    await room.connect(LIVEKIT_URL, token)

    # Kiểm tra agent đã join trước khi room.connect
    for identity, p in room.remote_participants.items():
        if "agent" in identity.lower() or p.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            pass

    return room, greeting_received, chat_reply_received, transcript_reply_received


# ---------------------------------------------------------------------------
# Hàm tiện ích: Gửi toggle web search qua kênh lk.control
# ---------------------------------------------------------------------------
async def send_web_search_toggle(room: rtc.Room, enabled: bool) -> None:
    payload = json.dumps({"type": "toggle_web_search", "enabled": enabled}).encode("utf-8")
    await room.local_participant.publish_data(payload, reliable=True, topic="lk.control")
    state = "BẬT ✅" if enabled else "TẮT ❌"
    print(f"   🔀 Đã gửi tín hiệu Toggle Web Search: {state}")


# ---------------------------------------------------------------------------
# Hàm tiện ích: Kiểm tra DB
# ---------------------------------------------------------------------------
async def check_db(thread_id: str, expected_min: int = 2) -> bool:
    async with aiohttp.ClientSession() as http:
        async with http.get(f"{BASE_URL}/threads/{thread_id}/messages") as r:
            msgs = await r.json()

    print(f"\n   🗄️  Database: {len(msgs)} tin nhắn")
    for m in msgs:
        role = "USER " if m["is_user"] else "AGENT"
        txt = m["text"]
        short = txt if len(txt) < 100 else txt[:100] + "..."
        print(f"      [{m['timestamp'][11:19]}] {role}: {short}")

    return len(msgs) >= expected_min


# ---------------------------------------------------------------------------
# TEST A: Toggle TẮT → Naive RAG (luồng mặc định, chỉ dùng sách)
# ---------------------------------------------------------------------------
async def test_naive_rag() -> bool:
    print("\n" + "=" * 60)
    print("  TEST A: Toggle TẮT → Naive RAG (tìm trong sách)")
    print("=" * 60)

    thread_id, token = await setup_session()
    print(f"   Thread ID: {thread_id}")

    room, greeting_ev, chat_ev, transcript_ev = await connect_room(token)

    print("   ⏳ Đợi Agent khởi động...")
    try:
        await asyncio.wait_for(greeting_ev.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        print("   ❌ Timeout: Agent không online.")
        await room.disconnect()
        return False

    # KHÔNG gửi toggle → mặc định TẮT (Naive RAG)
    print(f"   📤 Gửi câu hỏi trong sách: '{QUESTION_IN_BOOK}'")
    await room.local_participant.publish_data(
        QUESTION_IN_BOOK.encode("utf-8"), reliable=True, topic="lk.chat"
    )

    print("   ⏳ Chờ phản hồi (Naive RAG - chỉ tìm sách)...")
    success = False
    try:
        await asyncio.wait_for(chat_ev.wait(), timeout=30.0)
        await asyncio.wait_for(transcript_ev.wait(), timeout=5.0)
        print("   ✅ TEST A PASS: Nhận đủ phản hồi qua lk.chat + lk.transcript")
        success = True
    except asyncio.TimeoutError:
        print("   ❌ TEST A FAIL: Timeout chờ phản hồi")

    await room.disconnect()
    await asyncio.sleep(2)
    await check_db(thread_id, expected_min=3)
    return success


# ---------------------------------------------------------------------------
# TEST B: Toggle BẬT → Agentic Loop (LLM tự quyết định tìm web)
# ---------------------------------------------------------------------------
async def test_agentic_web_search() -> bool:
    print("\n" + "=" * 60)
    print("  TEST B: Toggle BẬT → Agentic Loop (LLM tự quyết định tìm web)")
    print("=" * 60)

    thread_id, token = await setup_session()
    print(f"   Thread ID: {thread_id}")

    room, greeting_ev, chat_ev, transcript_ev = await connect_room(token)

    print("   ⏳ Đợi Agent khởi động...")
    try:
        await asyncio.wait_for(greeting_ev.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        print("   ❌ Timeout: Agent không online.")
        await room.disconnect()
        return False

    # Bật toggle web search TRƯỚC khi gửi câu hỏi
    await send_web_search_toggle(room, enabled=True)
    await asyncio.sleep(0.5)  # Đợi server nhận tín hiệu toggle

    print(f"   📤 Gửi câu hỏi ngoài sách: '{QUESTION_OUTSIDE_BOOK}'")
    await room.local_participant.publish_data(
        QUESTION_OUTSIDE_BOOK.encode("utf-8"), reliable=True, topic="lk.chat"
    )

    # Chờ lâu hơn vì Agentic Loop cần gọi tool → LLM suy luận → web search
    print("   ⏳ Chờ phản hồi (Agentic Loop - có thể cần gọi web search)...")
    success = False
    try:
        await asyncio.wait_for(chat_ev.wait(), timeout=45.0)
        await asyncio.wait_for(transcript_ev.wait(), timeout=5.0)
        print("   ✅ TEST B PASS: Nhận đủ phản hồi qua lk.chat + lk.transcript")
        success = True
    except asyncio.TimeoutError:
        print("   ❌ TEST B FAIL: Timeout chờ phản hồi")

    await room.disconnect()
    await asyncio.sleep(2)
    await check_db(thread_id, expected_min=3)
    return success


# ---------------------------------------------------------------------------
# TEST C: Gửi nhiều câu hỏi thực tế liên tiếp để xác nhận web search chạy thật
# ---------------------------------------------------------------------------
async def test_web_search_verification() -> bool:
    print("\n" + "=" * 60)
    print("  TEST C: Xác minh Web Search thực tế (multi-question)")
    print("  ℹ️  Kiểm tra worker.log: tìm dòng 'Web Search (Tavily)'")
    print("  ℹ️  Đánh giá bằng mắt xem câu trả lời có chính xác không")
    print("=" * 60)

    thread_id, token = await setup_session()
    print(f"   Thread ID: {thread_id}")

    room = rtc.Room()
    greeting_received = asyncio.Event()
    # Queue nhận TẤT CẢ reply từ agent (trừ greeting) theo thứ tự đến
    reply_queue: asyncio.Queue[str] = asyncio.Queue()

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        if not packet.participant or "agent" not in packet.participant.identity.lower():
            return
        if packet.topic != "lk.chat":
            return
        try:
            text = packet.data.decode("utf-8")
        except Exception:
            return

        if not greeting_received.is_set():
            # Tin đầu tiên là greeting → đánh dấu agent online, không đưa vào queue
            print(f"   👋 Agent Greeting: {text[:100]}")
            greeting_received.set()
        else:
            # Các tin sau là reply cho câu hỏi → push vào queue
            reply_queue.put_nowait(text)

    await room.connect(LIVEKIT_URL, token)

    # Kiểm tra agent đã join trước khi connect
    for identity, p in room.remote_participants.items():
        if "agent" in identity.lower() or p.kind == rtc.ParticipantKind.PARTICIPANT_KIND_AGENT:
            pass

    print("   ⏳ Đợi Agent khởi động...")
    try:
        await asyncio.wait_for(greeting_received.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        print("   ❌ Timeout: Agent không online.")
        await room.disconnect()
        return False

    # Bật toggle web search
    await send_web_search_toggle(room, enabled=True)
    await asyncio.sleep(0.5)
    print("   🔀 Web Search: BẬT ✅\n")

    all_ok = True
    for i, question in enumerate(WEB_SEARCH_VERIFY_QUESTIONS, start=1):
        print(f"   {'─' * 50}")
        print(f"   Câu {i}/{len(WEB_SEARCH_VERIFY_QUESTIONS)}")
        print(f"   📤 Hỏi: {question}")

        await room.local_participant.publish_data(
            question.encode("utf-8"), reliable=True, topic="lk.chat"
        )

        try:
            # Lấy reply tiếp theo từ queue (chặn tối đa 45s)
            answer = await asyncio.wait_for(reply_queue.get(), timeout=45.0)
            print(f"   🤖 Trả lời ({len(answer)} ký tự):")
            for line in answer.split("\n"):
                print(f"      {line}")
            print()
        except asyncio.TimeoutError:
            print(f"   ❌ Timeout: Không nhận được phản hồi cho câu hỏi {i}\n")
            all_ok = False

        # Đợi ngắn giữa các câu để agent xử lý xong hoàn toàn
        await asyncio.sleep(1.5)

    await room.disconnect()
    await asyncio.sleep(2)
    await check_db(thread_id, expected_min=len(WEB_SEARCH_VERIFY_QUESTIONS) * 2 + 1)

    if all_ok:
        print("   ✅ TEST C PASS: Tất cả câu hỏi nhận được phản hồi.")
        print("   ⚠️  Đánh giá bằng mắt nội dung bên trên để xác nhận độ chính xác.")
    else:
        print("   ❌ TEST C FAIL: Có câu hỏi bị timeout.")
    return all_ok


# ---------------------------------------------------------------------------
# TEST D: Toggle cycle ON → OFF trong cùng phiên (tường minh test enabled=false)
# Mục tiêu: Xác nhận khi gửi toggle=false, AI quay lại Naive RAG và KHÔNG
# gọi web search nữa dù câu hỏi nằm ngoài sách.
# Cách verify: worker.log phải KHÔNG có dòng 'Web Search (Tavily)' sau lần tắt.
# ---------------------------------------------------------------------------
async def test_toggle_off_revert() -> bool:
    print("\n" + "=" * 60)
    print("  TEST D: Toggle Cycle ON → OFF trong cùng phiên")
    print("  ℹ️  Verify: worker.log KHÔNG có 'Web Search (Tavily)' ở câu hỏi thứ 2")
    print("=" * 60)

    thread_id, token = await setup_session()
    print(f"   Thread ID: {thread_id}")

    room = rtc.Room()
    greeting_received = asyncio.Event()
    reply_queue: asyncio.Queue[str] = asyncio.Queue()

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        if not packet.participant or "agent" not in packet.participant.identity.lower():
            return
        if packet.topic != "lk.chat":
            return
        try:
            text = packet.data.decode("utf-8")
        except Exception:
            return
        if not greeting_received.is_set():
            print(f"   👋 Agent Greeting: {text[:100]}")
            greeting_received.set()
        else:
            reply_queue.put_nowait(text)

    await room.connect(LIVEKIT_URL, token)

    print("   ⏳ Đợi Agent khởi động...")
    try:
        await asyncio.wait_for(greeting_received.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        print("   ❌ Timeout: Agent không online.")
        await room.disconnect()
        return False

    success = True

    # ── BƯỚC 1: Bật toggle, hỏi câu ngoài sách → phải dùng web search ──
    print()
    print("   [Bước 1] Bật toggle → BẬT ✅")
    await send_web_search_toggle(room, enabled=True)
    await asyncio.sleep(0.5)

    q1 = "Giá Bitcoin hôm nay là bao nhiêu USD?"
    print(f"   📤 Hỏi (Bước 1): {q1}")
    await room.local_participant.publish_data(q1.encode("utf-8"), reliable=True, topic="lk.chat")

    try:
        reply1 = await asyncio.wait_for(reply_queue.get(), timeout=45.0)
        print(f"   🤖 Trả lời Bước 1 ({len(reply1)} ký tự):")
        for line in reply1.split("\n"):
            print(f"      {line}")
        print(f"   ✅ Bước 1 OK – kiểm tra worker.log: phải có 'Web Search (Tavily)'")
    except asyncio.TimeoutError:
        print("   ❌ Bước 1 FAIL: Timeout")
        success = False

    await asyncio.sleep(1.5)

    # ── BƯỚC 2: TẮT toggle tường minh (enabled=false), hỏi lại → Naive RAG ──
    print()
    print("   [Bước 2] Tắt toggle → TẮT ❌")
    await send_web_search_toggle(room, enabled=False)  # <-- đây là điểm cần test
    await asyncio.sleep(0.5)

    q2 = "Giá Ethereum hôm nay là bao nhiêu USD?"
    print(f"   📤 Hỏi (Bước 2): {q2}")
    print(f"   ℹ️  Worker.log KHÔNG được có 'Web Search (Tavily)' sau dòng này")
    await room.local_participant.publish_data(q2.encode("utf-8"), reliable=True, topic="lk.chat")

    try:
        reply2 = await asyncio.wait_for(reply_queue.get(), timeout=30.0)
        print(f"   🤖 Trả lời Bước 2 ({len(reply2)} ký tự):")
        for line in reply2.split("\n"):
            print(f"      {line}")
        print(f"   ✅ Bước 2 OK – AI vẫn trả lời (từ sách hoặc training data, không dùng web)")
    except asyncio.TimeoutError:
        print("   ❌ Bước 2 FAIL: Timeout")
        success = False

    await room.disconnect()
    await asyncio.sleep(2)
    await check_db(thread_id, expected_min=5)  # greeting + 2 user + 2 agent

    if success:
        print()
        print("   ✅ TEST D PASS: Toggle cycle ON→OFF hoạt động đúng.")
        print("   ⚠️  Xác nhận bằng mắt: worker.log chỉ có 1 dòng 'Web Search' (Bước 1),")
        print("       KHÔNG có dòng 'Web Search' nào sau khi tắt toggle (Bước 2).")
    else:
        print("   ❌ TEST D FAIL")
    return success



async def main() -> None:
    print("=" * 60)
    print("  KIỂM THỬ: Toggle Web Search (Naive RAG vs Agentic Loop)")
    print("=" * 60)

    results: dict[str, bool] = {}
    results["TEST A (Naive RAG - default)"] = await test_naive_rag()
    results["TEST B (Toggle ON - Agentic)"] = await test_agentic_web_search()
    results["TEST C (Web Search multi-question)"] = await test_web_search_verification()
    results["TEST D (Toggle cycle ON→OFF)"] = await test_toggle_off_revert()

    print("\n" + "=" * 60)
    print("  KẾT QUẢ TỔNG HỢP")
    print("=" * 60)
    all_passed = True
    for name, passed in results.items():
        icon = "✅" if passed else "❌"
        print(f"  {icon}  {name}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 TẤT CẢ TEST PASS!")
        print("   → Hãy đánh giá thêm nội dung TEST C bằng mắt để xác nhận độ chính xác.")
    else:
        print("\n⚠️  Có test FAIL, kiểm tra log worker để debug.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Lỗi không mong đợi: {e}")
        sys.exit(1)
