"""
test_rag.py - Kiểm tra từng bước của pipeline RAG
Chạy: uv run python test_rag.py
"""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

# ─── BƯỚC 1: Kiểm tra biến môi trường ───────────────────────────────────────
print("=" * 60)
print("BƯỚC 1: Kiểm tra biến môi trường")
print("=" * 60)
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

print(f"  OPENAI_API_KEY    : {'✅ ' + OPENAI_KEY[:8] + '...' if OPENAI_KEY else '❌ MISSING'}")
print(f"  SUPABASE_URL      : {'✅ ' + SUPABASE_URL if SUPABASE_URL else '❌ MISSING'}")
print(f"  SUPABASE_KEY      : {'✅ ' + SUPABASE_KEY[:8] + '...' if SUPABASE_KEY else '❌ MISSING'}")

if not all([OPENAI_KEY, SUPABASE_URL, SUPABASE_KEY]):
    print("\n❌ Thiếu biến môi trường, dừng test.")
    exit(1)

# ─── BƯỚC 2: Kiểm tra dữ liệu trong bảng book_knowledge ─────────────────────
print("\n" + "=" * 60)
print("BƯỚC 2: Kiểm tra dữ liệu trong bảng book_knowledge")
print("=" * 60)
from supabase import create_client

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Đếm tổng số records
    count_result = sb.table("book_knowledge").select("id, book_id, content", count="exact").limit(5).execute()
    total = count_result.count
    sample = count_result.data
    print(f"  Tổng số records: {total}")
    if sample:
        print("  5 records đầu tiên:")
        for row in sample:
            print(f"    - book_id={row.get('book_id')} | id={row.get('id')} | content={str(row.get('content',''))[:60]}...")
    else:
        print("  ❌ Bảng book_knowledge RỖNG — chưa có dữ liệu được embed!")
except Exception as e:
    print(f"  ❌ Lỗi truy vấn bảng: {e}")
    exit(1)

# ─── BƯỚC 3: Lấy book_id thực tế để dùng cho test ───────────────────────────
print("\n" + "=" * 60)
print("BƯỚC 3: Lấy danh sách book_id có trong bảng")
print("=" * 60)
TEST_BOOK_ID = None
try:
    books = sb.table("book_knowledge").select("book_id").limit(100).execute()
    book_ids = list(set(r["book_id"] for r in books.data)) if books.data else []
    if book_ids:
        TEST_BOOK_ID = book_ids[0]
        print(f"  Tìm thấy {len(book_ids)} book_id: {book_ids}")
        print(f"  ➜ Sẽ dùng book_id = '{TEST_BOOK_ID}' để test RPC")
    else:
        print("  ❌ Không có book_id nào trong bảng — pipeline embed chưa chạy!")
except Exception as e:
    print(f"  ❌ Lỗi: {e}")

# ─── BƯỚC 4: Tạo embedding từ OpenAI ─────────────────────────────────────────
print("\n" + "=" * 60)
print("BƯỚC 4: Tạo embedding với OpenAI (text-embedding-3-small)")
print("=" * 60)

async def test_embedding():
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=OPENAI_KEY)
    try:
        test_query = "tri thức là gì"
        res = await client.embeddings.create(model="text-embedding-3-small", input=[test_query])
        vector = res.data[0].embedding
        print(f"  ✅ Embedding OK — query='{test_query}'")
        print(f"  Chiều vector: {len(vector)} (cần khớp với cột embedding trong DB)")
        return vector
    except Exception as e:
        print(f"  ❌ Lỗi OpenAI embedding: {e}")
        return None

query_vector = asyncio.run(test_embedding())

# ─── BƯỚC 5: Gọi RPC match_book_knowledge ────────────────────────────────────
print("\n" + "=" * 60)
print("BƯỚC 5: Gọi Supabase RPC match_book_knowledge")
print("=" * 60)

if query_vector is None:
    print("  ❌ Bỏ qua — không có embedding")
elif TEST_BOOK_ID is None:
    print("  ❌ Bỏ qua — không có book_id trong bảng")
else:
    # Test với threshold thấp trước (0.1) để chắc chắn có kết quả
    for threshold in [0.1, 0.3, 0.5]:
        try:
            result = sb.rpc("match_book_knowledge", {
                "query_embedding": query_vector,
                "match_threshold": threshold,
                "match_count": 3,
                "filter_book_id": TEST_BOOK_ID
            }).execute()

            if result.data:
                print(f"  ✅ threshold={threshold}: Tìm thấy {len(result.data)} kết quả")
                for i, item in enumerate(result.data, 1):
                    sim = item.get("similarity", "N/A")
                    content_preview = str(item.get("content", ""))[:80]
                    print(f"    [{i}] similarity={sim:.4f} | {content_preview}...")
                break
            else:
                print(f"  ⚠️  threshold={threshold}: Không có kết quả")
        except Exception as e:
            print(f"  ❌ Lỗi RPC (threshold={threshold}): {e}")
            break

# ─── BƯỚC 6: Test toàn bộ hàm search_book_knowledge ─────────────────────────
print("\n" + "=" * 60)
print("BƯỚC 6: Test hàm search_book_knowledge() end-to-end")
print("=" * 60)

async def test_search():
    if TEST_BOOK_ID is None:
        print("  ❌ Bỏ qua — không có book_id")
        return
    import sys
    sys.path.insert(0, ".")
    from app.services.rag_service import search_book_knowledge
    try:
        result = await search_book_knowledge("tri thức là gì", TEST_BOOK_ID)
        if result and result != "Không tìm thấy thông tin cụ thể trong sách.":
            print("  ✅ search_book_knowledge hoạt động!")
            print(f"  Kết quả:\n{result[:300]}...")
        else:
            print(f"  ⚠️  Trả về: '{result}'")
            print("  → Dữ liệu có thể chưa được embed hoặc threshold quá cao")
    except Exception as e:
        print(f"  ❌ Lỗi: {e}")

asyncio.run(test_search())

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
