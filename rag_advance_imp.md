# RAG Advance Implementation

## 🛠️ Giai đoạn 1: Làm giàu dữ liệu (Data Enrichment & Smart Chunking)

**Vấn đề:** Các đoạn văn (chunks) thô thường bị mất ngữ cảnh nếu đứng một mình (ví dụ: đoạn văn nói về "ông ấy" nhưng không biết "ông ấy" là ai).

**Giải pháp:** Bơm metadata (tên sách, tên chương) trực tiếp vào nội dung chunk trước khi tạo Embedding.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_book_to_enriched_chunks(book_title: str, chapter_title: str, raw_text: str):
    # 1. Sử dụng RecursiveCharacterTextSplitter để ngắt đoạn thông minh theo dấu câu
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )

    raw_chunks = text_splitter.split_text(raw_text)
    enriched_chunks = []

    for index, chunk in enumerate(raw_chunks):
        # BƠM NGỮ CẢNH: Giúp Vector nắm bắt được bối cảnh toàn cục
        header = f"[Tác phẩm: {book_title} | Chương: {chapter_title}]\n"
        enriched_content = header + chunk

        enriched_chunks.append({
            "content": enriched_content,
            "metadata": {
                "chapter": chapter_title,
                "chunk_index": index
            }
        })

    return enriched_chunks
```

> **💡 Tại sao làm vậy?** Khi em search "nhân vật chính", Vector Database sẽ tìm thấy các đoạn có chữ "nhân vật" nằm ngay cạnh tiêu đề "Sách: Bí mật của một trí nhớ siêu phàm". Độ khớp sẽ cao hơn hẳn so với việc chỉ lưu văn bản thô.

---

## 🧠 Giai đoạn 2 & 3: Query Rewriting (Tinh chỉnh câu hỏi)

**Vấn đề:** User thường hỏi rất ngắn ("Nội dung chính?", "Tác giả là ai?"). Vector DB rất khó để khớp những từ khóa quá ngắn này.

**Giải pháp:** Dùng Gemini 2.5 Flash để "thổi phồng" câu hỏi thành một truy vấn đầy đủ ngữ cảnh.

```python
import google.generativeai as genai

# Dùng model Flash để lấy Latency thấp nhất
model = genai.GenerativeModel('gemini-2.5-flash')

async def rewrite_query_for_triam(raw_query: str, book_title: str) -> str:
    # Nếu câu hỏi đã đủ dài (> 12 từ), không cần rewrite để tiết kiệm latency
    if len(raw_query.split()) > 12:
        return raw_query

    prompt = f"""
    Bạn là chuyên gia xử lý ngôn ngữ cho hệ thống TRIAM.
    Người dùng đang đọc sách "{book_title}" và đặt câu hỏi: "{raw_query}".
    Hãy viết lại câu hỏi này thành một truy vấn đầy đủ ngữ cảnh, chứa tên sách và các từ khóa liên quan để công cụ tìm kiếm Vector có thể hoạt động chính xác nhất.
    YÊU CẦU: Chỉ trả về câu hỏi mới, không giải thích.
    """

    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except:
        return raw_query # Fallback
```

---

## 🔥 Giai đoạn 4: Hybrid Search & Multilingual Reranking

Đây là trái tim của hệ thống. Chúng ta sẽ dùng **BAAI/bge-reranker-v2-m3** vì đây là model hỗ trợ **Tiếng Việt** và đa ngôn ngữ tốt nhất hiện nay.

**Bước 4.1: Cài đặt môi trường**
Sử dụng `uv` để quản lý thư viện nhẹ nhàng và nhanh chóng.

```bash
uv add sentence-transformers torch
```

**Bước 4.2: Implement luồng tìm kiếm nâng cao**

```python
import torch
from sentence_transformers import CrossEncoder
from app.core.supabase import supabase

# Tải model reranker (Hỗ trợ context lên đến 8192 tokens)
device = "cuda" if torch.cuda.is_available() else "cpu"
reranker = CrossEncoder('BAAI/bge-reranker-v2-m3', device=device)

async def advanced_triam_rag(raw_query: str, book_id: str, book_title: str):
    # 1. Viết lại câu hỏi (Stage 3)
    smart_query = await rewrite_query_for_triam(raw_query, book_title)

    # 2. Tạo Embedding cho câu hỏi đã rewrite
    # (Giả sử em đã có hàm tạo embedding từ OpenAI)
    query_vector = await generate_embedding(smart_query)

    # 3. Retrieval: Lấy 15-20 kết quả thô từ Supabase (Stage 2)
    # Nới lỏng match_threshold để reranker có dữ liệu làm việc
    db_results = supabase.rpc('match_book_knowledge', {
        'query_embedding': query_vector,
        'match_threshold': 0.15,
        'match_count': 20,
        'filter_book_id': str(book_id)
    }).execute()

    if not db_results.data:
        return "Xin lỗi, mình không tìm thấy thông tin này trong tài liệu."

    # 4. Reranking: Chốt chặn cuối cùng (Stage 4)
    # Cross-Encoder sẽ chấm điểm độ liên quan trực tiếp giữa (Câu hỏi, Đoạn văn)
    pairs = [[smart_query, row['content']] for row in db_results.data]

    with torch.no_grad():
        scores = reranker.predict(pairs)

    # Ghép điểm và sắp xếp lại
    for i, row in enumerate(db_results.data):
        row['rerank_score'] = float(scores[i])

    # Sắp xếp theo điểm số rerank giảm dần
    sorted_results = sorted(db_results.data, key=lambda x: x['rerank_score'], reverse=True)

    # 5. Lọc kết quả chất lượng cao
    # Nếu điểm rerank quá thấp (< 0.3), có thể coi là không liên quan
    final_context = [res for res in sorted_results if res['rerank_score'] > 0.3][:3]

    return final_context
```
