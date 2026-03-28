import os

from openai import AsyncOpenAI
from pinecone import Pinecone

from app.core.supabase import supabase

# Khởi tạo OpenAI
aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Khởi tạo Pinecone (Client v3+)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = "triam-knowledge-base"  # Tên Index bạn đã tạo trên Web Console
index = pc.Index(INDEX_NAME)


async def embed_chunk_to_supbabase(book_id: str, chapter_index: int, chunks: list[str]):
    try:
        response = await aclient.embeddings.create(
            input=chunks,
            model="text-embedding-3-small"
        )

        data_to_insert = []
        for i, embedding_data in enumerate(response.data):
            data_to_insert.append({
                "book_id": book_id,
                "chapter_index": chapter_index,
                "chunk_index": i,
                "content": chunks[i],
                "embedding": embedding_data.embedding
            })

        # Insert vào Supabase
        if data_to_insert:
            supabase.table("book_knowledge").insert(data_to_insert).execute()
            print(f"✅ Saved {len(data_to_insert)} vectors into Supabase.")
            return True

    except Exception as e:
        print(f"Error Embed Supabase: {e}")
        return False



# ====== OLD CODE ======
async def embed_text_to_pinecone(book_id: str, chapter_index: int, text: str):
    """
    Hàm xử lý RAG: Cắt nhỏ text -> Embed -> Lưu vào Pinecone.
    """
    try:
        # 1. CHUNKING (Cắt nhỏ văn bản)
        # Tại sao cần cắt? Vì Vector search hoạt động tốt nhất với các đoạn văn ngắn (context).
        # Cách đơn giản: Cắt theo đoạn văn (xuống dòng kép)
        chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 50]

        # Nếu text không có xuống dòng, cắt thô mỗi 1000 ký tự (Fallback)
        if not chunks:
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        print(f"-> Pinecone: Đang xử lý {len(chunks)} chunks cho chương {chapter_index + 1}...")

        vectors_to_upsert = []

        # 2. EMBEDDING (Tạo vector)
        # OpenAI hỗ trợ batch embedding, ta gửi cả list chunks đi 1 lần cho nhanh
        response = await aclient.embeddings.create(
            input=chunks,
            model="text-embedding-3-small" # Rẻ và nhanh, đủ dùng cho RAG
        )

        # 3. CHUẨN BỊ DATA (Format cho Pinecone)
        for i, embedding_data in enumerate(response.data):
            chunk_text = chunks[i]
            vector_id = f"{book_id}_chap{chapter_index}_{i}" # ID duy nhất

            # Vector Record
            vector_record = {
                "id": vector_id,
                "values": embedding_data.embedding,
                # Metadata cực quan trọng để AI biết đoạn này là chữ gì
                "metadata": {
                    "book_id": book_id,
                    "chapter_index": chapter_index,
                    "text": chunk_text, # Lưu text gốc để hồi đáp user
                    "source": "triam_app"
                }
            }
            vectors_to_upsert.append(vector_record)

        # 4. UPSERT (Đẩy lên Cloud)
        # Sử dụng namespace để tách biệt dữ liệu (optional, nhưng recommend)
        # Namespace giúp bạn xóa sách dễ dàng: index.delete(delete_all=True, namespace=book_id)
        index.upsert(vectors=vectors_to_upsert, namespace=book_id)

        print(f"-> Pinecone: Đã lưu {len(vectors_to_upsert)} vectors vào namespace '{book_id}'.")
        return True

    except Exception as e:
        print(f"Lỗi Embed Pinecone: {e}")
        return False
