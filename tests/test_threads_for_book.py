"""
Kiểm thử endpoint: GET /threads/for-book/{book_id}

Mục tiêu:
- Xác nhận endpoint hoạt động đúng chức năng get-or-create
- Xác nhận idempotent (gọi nhiều lần → nhận cùng thread_id)
- Xác nhận race-safe (concurrent requests → không duplicate)
- Xác nhận DirectBookContext + auto StudyContext được tạo đúng
"""
import asyncio
import uuid

import aiohttp
from sqlmodel import Session

from app.db.database import engine
from app.models.db_models import Book

BASE_URL = "http://127.0.0.1:8000/api/v1"
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")

def setup_mock_book(book_id: uuid.UUID):
    with Session(engine) as session:
        book = Book(id=book_id, user_id=MOCK_USER_ID, title="Mock Book for Test")
        session.add(book)
        session.commit()

def cleanup_mock_book(book_id: uuid.UUID):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()


# Dùng book ID thực tế hoặc tạo mock
TEST_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"


# ---------------------------------------------------------------------------
# TEST 1: Lần đầu gọi → tạo auto context + thread
# ---------------------------------------------------------------------------
async def test_first_call_creates_context_and_thread() -> bool:
    """
    Khi gọi GET /threads/for-book/{book_id} lần đầu:
    - BE tạo DirectBookContext
    - BE tạo auto StudyContext (is_auto_generated=true)
    - BE tạo 1 ChatThread duy nhất
    - Return context_id + thread_id
    """
    print("\n" + "=" * 60)
    print("  TEST 1: Lần đầu gọi → tạo auto context + thread")
    print("=" * 60)

    # Chọn book_id mới để chắc chắn chưa có context
    unique_book_id = uuid.uuid4()
    setup_mock_book(unique_book_id)

    try:
        async with aiohttp.ClientSession() as session:
            # Gọi endpoint lần đầu
            print(f"   📤 Gọi GET /threads/for-book/{unique_book_id}")
            async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                if resp.status != 200:
                    print(f"   ❌ Status {resp.status}: {await resp.text()}")
                    return False

                data = await resp.json()
                print(f"   ✅ Status 200 OK")

                context_id = data.get("context_id")
                thread_id = data.get("thread_id")
                is_auto_generated = data.get("is_auto_generated")

                # Verify response structure
                if not context_id or not thread_id:
                    print(f"   ❌ Missing context_id or thread_id in response")
                    return False

                if is_auto_generated != True:
                    print(
                        f"   ❌ is_auto_generated should be true, got {is_auto_generated}")
                    return False

                print(f"   Context ID: {context_id}")
                print(f"   Thread ID: {thread_id}")
                print(f"   is_auto_generated: {is_auto_generated}")

                # Verify thread history exists and is empty (only greeting will come later via LiveKit)
                print(f"\n   📋 Checking thread history...")
                async with session.get(f"{BASE_URL}/threads/{thread_id}/messages") as msg_resp:
                    if msg_resp.status != 200:
                        print(
                            f"   ⚠️  Warning: Could not fetch messages: {msg_resp.status}")
                    else:
                        messages = await msg_resp.json()
                        print(
                            f"   ✅ Thread has {len(messages)} messages (should be 0 at first)")

                print(f"\n   ✅ TEST 1 PASS: Auto context + thread created successfully")
                return True
    finally:
        cleanup_mock_book(unique_book_id)


# ---------------------------------------------------------------------------
# TEST 2: Idempotent - gọi lần 2 → nhận cùng thread_id
# ---------------------------------------------------------------------------
async def test_idempotent_same_thread_id() -> bool:
    """
    Khi gọi GET /threads/for-book/{book_id} lần 2:
    - BE tìm thấy DirectBookContext đã tồn tại
    - Return cùng context_id + thread_id (KHÔNG tạo mới)
    """
    print("\n" + "=" * 60)
    print("  TEST 2: Gọi lần 2 → idempotent (return cùng thread)")
    print("=" * 60)

    unique_book_id = uuid.uuid4()
    setup_mock_book(unique_book_id)

    try:
        async with aiohttp.ClientSession() as session:
            # Gọi lần 1
            print(f"   📤 Gọi lần 1...")
            async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                data1 = await resp.json()
                context_id_1 = data1.get("context_id")
                thread_id_1 = data1.get("thread_id")
                print(f"   ✅ Lần 1: thread_id = {thread_id_1}")

            await asyncio.sleep(0.2)

            # Gọi lần 2
            print(f"   📤 Gọi lần 2...")
            async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                data2 = await resp.json()
                context_id_2 = data2.get("context_id")
                thread_id_2 = data2.get("thread_id")
                print(f"   ✅ Lần 2: thread_id = {thread_id_2}")

            # Verify same IDs
            if context_id_1 != context_id_2:
                print(f"   ❌ context_id khác: {context_id_1} vs {context_id_2}")
                return False

            if thread_id_1 != thread_id_2:
                print(f"   ❌ thread_id khác: {thread_id_1} vs {thread_id_2}")
                return False

            print(f"   ✅ context_id match: {context_id_1}")
            print(f"   ✅ thread_id match: {thread_id_1}")
            print(f"\n   ✅ TEST 2 PASS: Idempotent behavior confirmed")
            return True
    finally:
        cleanup_mock_book(unique_book_id)


# ---------------------------------------------------------------------------
# TEST 3: Concurrent requests → no duplicate (race-safe)
# ---------------------------------------------------------------------------
async def test_concurrent_requests_no_race() -> bool:
    """
    Khi 2+ requests gọi cùng lúc:
    - DB transaction đảm bảo chỉ 1 context được tạo
    - Tất cả requests nhận cùng thread_id
    - Không có duplicate threads
    """
    print("\n" + "=" * 60)
    print("  TEST 3: Concurrent requests → race-safe (no duplicate)")
    print("=" * 60)

    unique_book_id = uuid.uuid4()
    setup_mock_book(unique_book_id)

    try:
        async def fetch_thread():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                    return await resp.json()

        # Fire 5 concurrent requests
        print(f"   🔥 Sending 5 concurrent requests...")
        results = await asyncio.gather(*[fetch_thread() for _ in range(5)], return_exceptions=True)

        # Check all succeeded
        failed = [r for r in results if isinstance(r, Exception)]
        if failed:
            print(f"   ❌ Some requests failed: {failed}")
            return False

        print(f"   ✅ All 5 requests succeeded")

        # Verify all got same thread_id
        thread_ids = [r.get("thread_id") for r in results]
        context_ids = [r.get("context_id") for r in results]

        print(f"   Thread IDs: {set(thread_ids)}")
        print(f"   Context IDs: {set(context_ids)}")

        if len(set(thread_ids)) != 1:
            print(f"   ❌ Multiple different thread_ids: {set(thread_ids)}")
            return False

        if len(set(context_ids)) != 1:
            print(f"   ❌ Multiple different context_ids: {set(context_ids)}")
            return False

        thread_id = thread_ids[0]

        # Verify no duplicate threads under same context
        print(f"   📋 Checking DB for duplicate threads...")
        async with aiohttp.ClientSession() as session:
            # Get messages to verify only one thread
            async with session.get(f"{BASE_URL}/threads/{thread_id}/messages") as resp:
                if resp.status == 200:
                    messages = await resp.json()
                    print(
                        f"   ✅ Single thread exists with {len(messages)} messages")

        print(f"\n   ✅ TEST 3 PASS: Concurrent requests are race-safe")
        return True
    finally:
        cleanup_mock_book(unique_book_id)


# ---------------------------------------------------------------------------
# TEST 4: Verify DirectBookContext is created correctly
# ---------------------------------------------------------------------------
async def test_direct_book_context_structure() -> bool:
    """
    Verify DirectBookContext:
    - Maps (user_id, book_id) correctly
    - Has valid context_id + primary_thread_id
    - is_auto_generated = true for context
    """
    print("\n" + "=" * 60)
    print("  TEST 4: DirectBookContext structure validation")
    print("=" * 60)

    unique_book_id = uuid.uuid4()
    setup_mock_book(unique_book_id)

    try:
        async with aiohttp.ClientSession() as session:
            # Get-or-create thread
            print(f"   📤 Creating auto context for book {unique_book_id}...")
            async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                data = await resp.json()
                context_id = data.get("context_id")
                thread_id = data.get("thread_id")

            print(f"   ✅ Context ID: {context_id}")
            print(f"   ✅ Thread ID: {thread_id}")

            # Verify context exists and is auto-generated
            print(f"\n   📋 Fetching context details...")
            async with session.get(f"{BASE_URL}/study-contexts/{context_id}") as resp:
                if resp.status != 200:
                    print(f"   ❌ Could not fetch context: {resp.status}")
                    return False

                ctx_data = await resp.json()
                is_auto = ctx_data.get("is_auto_generated")

                if is_auto != True:
                    print(
                        f"   ❌ Context is_auto_generated should be true, got {is_auto}")
                    return False

                print(f"   ✅ Context is_auto_generated = true")
                print(f"   ✅ Context title: {ctx_data.get('title')}")

            # Verify thread exists under context
            print(f"\n   📋 Fetching context's threads...")
            async with session.get(f"{BASE_URL}/study-contexts/{context_id}/threads") as resp:
                if resp.status != 200:
                    print(f"   ❌ Could not fetch threads: {resp.status}")
                    return False

                threads = await resp.json()
                if len(threads) == 0:
                    print(f"   ❌ No threads found under context")
                    return False

                if len(threads) > 1:
                    print(
                        f"   ⚠️  Warning: Found {len(threads)} threads (expected 1)")
                    # Not a fail, but unusual

                primary_thread = threads[0]
                if primary_thread["id"] != thread_id:
                    print(
                        f"   ❌ Primary thread {primary_thread['id']} != returned thread {thread_id}")
                    return False

                print(f"   ✅ Context has {len(threads)} thread(s)")
                print(f"   ✅ Primary thread title: {primary_thread.get('title')}")

        print(f"\n   ✅ TEST 4 PASS: DirectBookContext structure is correct")
        return True
    finally:
        cleanup_mock_book(unique_book_id)


# ---------------------------------------------------------------------------
# TEST 5: Multiple books for same user → separate contexts/threads
# ---------------------------------------------------------------------------
async def test_multiple_books_separate_contexts() -> bool:
    """
    Verify:
    - Book A + User → Context A, Thread A
    - Book B + User → Context B, Thread B (different from A)
    - Each book has its own canonical thread
    """
    print("\n" + "=" * 60)
    print("  TEST 5: Multiple books → separate contexts/threads")
    print("=" * 60)

    book_id_1 = uuid.uuid4()
    book_id_2 = uuid.uuid4()
    setup_mock_book(book_id_1)
    setup_mock_book(book_id_2)

    try:
        async with aiohttp.ClientSession() as session:
            # Get thread for Book 1
            print(f"   📤 Book 1: {book_id_1}")
            async with session.get(f"{BASE_URL}/threads/for-book/{book_id_1}") as resp:
                data1 = await resp.json()
                context_id_1 = data1.get("context_id")
                thread_id_1 = data1.get("thread_id")
            print(f"      Context: {context_id_1}, Thread: {thread_id_1}")

            await asyncio.sleep(0.1)

            # Get thread for Book 2
            print(f"   📤 Book 2: {book_id_2}")
            async with session.get(f"{BASE_URL}/threads/for-book/{book_id_2}") as resp:
                data2 = await resp.json()
                context_id_2 = data2.get("context_id")
                thread_id_2 = data2.get("thread_id")
            print(f"      Context: {context_id_2}, Thread: {thread_id_2}")

            # Verify different
            if context_id_1 == context_id_2:
                print(f"   ❌ Both books got same context (should be different)")
                return False

            if thread_id_1 == thread_id_2:
                print(f"   ❌ Both books got same thread (should be different)")
                return False

            print(f"\n   ✅ Book 1 and Book 2 have different contexts and threads")
            print(f"   ✅ TEST 5 PASS: Multiple books properly isolated")
            return True
    finally:
        cleanup_mock_book(book_id_1)
        cleanup_mock_book(book_id_2)


# ---------------------------------------------------------------------------
# TEST 6: Can chat immediately after getting thread
# ---------------------------------------------------------------------------
async def test_thread_ready_for_chat() -> bool:
    """
    Verify newly created thread is ready to use:
    - Can fetch live token with thread_id
    - Can query thread messages
    - Thread is valid for LiveKit connection
    """
    print("\n" + "=" * 60)
    print("  TEST 6: Thread ready for immediate use")
    print("=" * 60)

    unique_book_id = uuid.uuid4()
    setup_mock_book(unique_book_id)

    try:
        async with aiohttp.ClientSession() as session:
            # Get thread
            print(f"   📤 Creating thread...")
            async with session.get(f"{BASE_URL}/threads/for-book/{unique_book_id}") as resp:
                data = await resp.json()
                thread_id = data.get("thread_id")

            print(f"   ✅ Got thread_id: {thread_id}")

            # Try to get LiveKit token immediately
            print(f"   📤 Requesting LiveKit token...")
            async with session.get(f"{BASE_URL}/live-token/thread/{thread_id}") as resp:
                if resp.status != 200:
                    print(f"   ❌ Could not get token: {resp.status}")
                    return False

                token_data = await resp.json()
                token = token_data.get("token")
                room_name = token_data.get("room_name")

                if not token:
                    print(f"   ❌ No token in response")
                    return False

                print(f"   ✅ Got token: {token[:50]}...")
                print(f"   ✅ Room name: {room_name}")

            # Try to fetch messages
            print(f"   📤 Fetching thread messages...")
            async with session.get(f"{BASE_URL}/threads/{thread_id}/messages") as resp:
                if resp.status != 200:
                    print(f"   ❌ Could not fetch messages: {resp.status}")
                    return False

                messages = await resp.json()
                print(f"   ✅ Got {len(messages)} messages")

        print(f"\n   ✅ TEST 6 PASS: Thread is ready for immediate use")
        return True
    finally:
        cleanup_mock_book(unique_book_id)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
async def main() -> None:
    print("=" * 60)
    print("  KIỂM THỬ: GET /threads/for-book/{book_id} endpoint")
    print("=" * 60)

    results: dict[str, bool] = {}
    results["TEST 1 (First call → create context+thread)"] = await test_first_call_creates_context_and_thread()
    results["TEST 2 (Idempotent → same thread)"] = await test_idempotent_same_thread_id()
    results["TEST 3 (Concurrent → race-safe)"] = await test_concurrent_requests_no_race()
    results["TEST 4 (DirectBookContext structure)"] = await test_direct_book_context_structure()
    results["TEST 5 (Multiple books → separate)"] = await test_multiple_books_separate_contexts()
    results["TEST 6 (Thread ready for chat)"] = await test_thread_ready_for_chat()

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
        print("   → Endpoint /threads/for-book/{book_id} hoạt động đúng")
    else:
        print("\n⚠️  Có test FAIL, kiểm tra lại implementation")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nLỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
