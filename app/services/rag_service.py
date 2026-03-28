from openai import AsyncOpenAI

from app.core.config import settings
from app.core.supabase import supabase

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def search_book_knowledge(query: str, book_id: str):
    # 1. Tạo embedding cho câu hỏi của user
    res = await ai_client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC match_book_knowledge đã tạo ở Supabase
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.2,
        "match_count": 3,
        "filter_book_id": book_id
    }).execute()

    if not result.data:
        return "Không tìm thấy thông tin cụ thể trong sách."

    return "\n".join([item['content'] for item in result.data])
