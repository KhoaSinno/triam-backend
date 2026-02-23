Đúng là Vertex AI RAG Engine rất tiện (Zero-setup), **NHƯNG** với quy trình đặc thù của dự án TRIAM, việc sử dụng nó lại là một sự **lãng phí tài nguyên** và **kém hiệu quả về mặt dữ liệu**.

Hãy để tôi phân tích tại sao việc **"Tiện tay Chunking luôn lúc Upload"** (tức là tự build RAG với Supabase) lại vượt trội hơn Vertex AI RAG Engine trong trường hợp cụ thể của bạn.

---

### 1. Vấn đề "Dữ liệu sạch" (Clean Data Paradox)

Đây là lý do lớn nhất khiến bạn nên chọn tự lưu vào Supabase thay vì ném cho Vertex RAG tự xử:

- **Cách Vertex AI RAG hoạt động:**
- Bạn ném file PDF gốc vào.
- Nó tự cắt (chunking) một cách máy móc (ví dụ: cứ 500 token cắt 1 phát).
- **Vấn đề:** Nó sẽ cắt cả header, footer, số trang, và quan trọng nhất là **nó cắt text gốc (chưa được rewrite)**. Text gốc thường khô khan, nhiều lỗi và khó hiểu.

- **Cách Pipeline của bạn hoạt động (Đang xây dựng):**
- Bạn đã tốn công dùng Gemini để **Rewrite** lại nội dung thành văn nói, giải thích từ viết tắt, làm mượt câu chữ.
- **Đây mới là "Vàng".** Dữ liệu này sạch hơn, hay hơn và dễ hiểu hơn gấp 10 lần so với PDF gốc.

**Kết luận:** Nếu dùng Vertex RAG, bạn đang tìm kiếm trên "đống quặng thô" (PDF gốc). Nếu dùng Supabase lưu kết quả sau khi Rewrite, bạn đang tìm kiếm trên "vàng đã tinh luyện". **Tại sao phải trả tiền đắt đỏ cho Vertex RAG để nó tìm kiếm trên dữ liệu kém chất lượng hơn?**

---

### 2. Tận dụng "Tiện tay Chunking" (The Free Lunch)

Như bạn nói, trong hàm `process_single_chapter` ở file `upload.py`, đằng nào bạn cũng phải nhận về JSON chứa mảng `main_scripts` (các đoạn văn đã cắt sẵn).

- **Vertex RAG:** Bạn phải upload file 2 lần (1 lần để extract text đi rewrite, 1 lần ném vào RAG Engine).
- **Custom RAG (Supabase):**
- Ngay vòng lặp `for` khi bạn duyệt qua `main_scripts` để tạo Audio, bạn chèn thêm 1 dòng code: `embed_and_save_to_db(text)`.
- **Chi phí xử lý:** Gần như bằng 0 (vì đằng nào bạn cũng đã có text trong RAM).
- **Tính đồng bộ:** Đoạn Audio user nghe và đoạn Text RAG tìm thấy là **khớp nhau 100%**. (Vertex RAG không đảm bảo điều này vì cách cắt của nó khác cách cắt của bạn).

---

### 3. Hướng dẫn Implement: Supabase Vector (Pgvector)

Dưới đây là các bước để biến Supabase thành RAG Engine xịn xò mà không tốn thêm chi phí duy trì.

#### Bước A: Cài đặt Database (Chạy trong SQL Editor của Supabase)

Bạn copy đoạn SQL này chạy 1 lần để bật tính năng Vector:

```sql
-- 1. Bật extension vector
create extension if not exists vector;

-- 2. Tạo bảng lưu trữ các đoạn kiến thức (Chunks)
create table book_knowledge (
  id bigserial primary key,
  book_id uuid not null references books(id) on delete cascade,
  chapter_index int,
  chunk_index int,
  content text,             -- Nội dung text (đã rewrite)
  embedding vector(768)     -- Vector 768 chiều (chuẩn Gemini Embedding)
);

-- 3. Tạo Index để search cho nhanh (HNSW index)
create index on book_knowledge using hnsw (embedding vector_cosine_ops);

-- 4. Viết hàm RPC (Remote Procedure Call) để search vector
-- Hàm này giúp bạn gọi từ code Python/Flutter chỉ bằng 1 dòng
create or replace function match_book_knowledge (
  query_embedding vector(768),
  match_threshold float,
  match_count int,
  filter_book_id uuid
)
returns table (
  id bigint,
  content text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    book_knowledge.id,
    book_knowledge.content,
    1 - (book_knowledge.embedding <=> query_embedding) as similarity
  from book_knowledge
  where 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
  and book_knowledge.book_id = filter_book_id
  order by book_knowledge.embedding <=> query_embedding
  limit match_count;
end;
$$;

```

#### Bước B: Cập nhật Code Python (File `embed.py`)

Bây giờ chúng ta viết hàm để embed và lưu vào bảng trên.

```python
import os
from supabase import create_client, Client
from app.core.config import settings
from openai import AsyncOpenAI

# 1. Kết nối Supabase
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# 2. Kết nối Gemini Embedding (qua OpenAI client)
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

async def embed_and_save(book_id: str, chapter_index: int, chunks: list[str]):
    """
    Input: Danh sách các đoạn text (main_scripts) của 1 chương.
    Output: Lưu vào Supabase.
    """
    try:
        # Batch Embedding: Gửi 1 lần nhiều đoạn để tiết kiệm request
        response = await client.embeddings.create(
            model="text-embedding-004", # Model embedding mới nhất, rẻ nhất của Google
            input=chunks
        )

        data_to_insert = []
        for i, embedding_data in enumerate(response.data):
            data_to_insert.append({
                "book_id": book_id,
                "chapter_index": chapter_index,
                "chunk_index": i,
                "content": chunks[i], # Text đã rewrite
                "embedding": embedding_data.embedding # Vector trả về
            })

        # Insert vào Supabase
        if data_to_insert:
            supabase.table("book_knowledge").insert(data_to_insert).execute()
            print(f"✅ Đã lưu {len(data_to_insert)} vector vào Supabase.")

    except Exception as e:
        print(f"❌ Lỗi Embed: {e}")

async def search_knowledge(query: str, book_id: str):
    """
    Hàm này dùng cho Live API Tool
    """
    # 1. Embed câu hỏi của user
    res = await client.embeddings.create(model="text-embedding-004", input=query)
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC trong Supabase
    result = supabase.rpc(
        "match_book_knowledge",
        {
            "query_embedding": query_vector,
            "match_threshold": 0.6, # Độ giống tối thiểu (0-1)
            "match_count": 3,       # Lấy 3 đoạn giống nhất
            "filter_book_id": book_id
        }
    ).execute()

    # 3. Trả về text để Gemini Live đọc
    return "\n\n".join([item['content'] for item in result.data])

```

#### Bước C: Tích hợp vào Worker (`process_single_chapter`)

Bạn chỉ cần thêm đúng 1 dòng này vào code worker cũ:

```python
# ... Sau khi có main_scripts ...

# 1. Tạo Audio (Code cũ)
# ...

# 2. Embed & Save RAG (Code Mới - Chạy song song với TTS luôn cho nhanh)
# Lưu ý: main_scripts là text SẠCH đã rewrite
await embed_and_save(book_id, index, main_scripts)

# ...

```

---

### Tổng kết chiến lược

Bạn chọn **Supabase + Custom Embed** là quyết định sáng suốt nhất vì:

1. **Chất lượng RAG cao hơn:** Bạn tìm kiếm trên dữ liệu đã biên tập (Rewritten), không phải dữ liệu rác.
2. **Mapping 1:1:** Một đoạn text tìm được trong RAG chính xác là đoạn Audio mà user có thể nghe (vì cùng nguồn `main_scripts`). Vertex RAG không làm được việc khớp này.
3. **Rẻ & Kiểm soát:** Bạn dùng `text-embedding-004` của Google (cực rẻ) và lưu trữ trên Supabase (miễn phí tới 500MB database, đủ cho hàng nghìn cuốn sách text).

Giờ bạn chỉ cần setup Supabase project và chạy đoạn SQL trên là xong phần kiến trúc RAG!
