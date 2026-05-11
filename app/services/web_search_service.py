from tavily import AsyncTavilyClient

from app.core.config import settings
from app.core.logger import log

# Singleton async client
_tavily_client: AsyncTavilyClient | None = None


def get_tavily_client() -> AsyncTavilyClient:
    global _tavily_client
    if _tavily_client is None:
        if not settings.TAVILY_API_KEY:
            raise RuntimeError("Thiếu TAVILY_API_KEY trong cấu hình!")
        _tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
    return _tavily_client


async def search_web(query: str, max_results: int = 3) -> str:
    """
    Tìm kiếm web bằng Tavily AsyncClient (Tối ưu cho LLM Agents).
    Trả về chuỗi văn bản đã được format để tiết kiệm token cho AI.
    """
    log.info(f"Web Search (Tavily): {query}")

    try:
        client = get_tavily_client()
        response = await client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
        )

        results = response.get("results", [])
        if not results:
            return "Không tìm thấy thông tin trên internet cho câu hỏi này."

        formatted_results = [
            f"- {item.get('title', '')}: {item.get('content', '')}"
            for item in results
        ]
        return "\n".join(formatted_results)

    except Exception as e:
        log.error(f"Lỗi khi search web: {str(e)}")
        return "Đã xảy ra lỗi hệ thống khi kết nối internet."
