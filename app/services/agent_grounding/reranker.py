from app.core.logger import log
from app.core.config import settings
from typing import Any
import httpx
import asyncio

async def rerank_candidates(
    query: str,
    candidates: list[dict[str, Any]],
    *,
    model: str | None = None,
    top_n: int | None = None
) -> list[dict[str, Any]]:
    """
    Sử dụng Cohere Multilingual Rerank API v2 để xếp hạng lại (Rerank) các chunks ứng viên.
    
    Args:
        query: Câu hỏi hoặc truy vấn của người dùng.
        candidates: Danh sách các chunk ứng viên dạng dictionary từ Hybrid Retrieval.
        model: Model rerank sử dụng (mặc định lấy từ settings).
        top_n: Số lượng kết quả tối đa muốn giữ lại (mặc định lấy từ settings).
        
    Returns:
        Danh sách các chunk đã được cập nhật score và sắp xếp theo thứ tự giảm dần.
        Nếu API lỗi hoặc không cấu hình API Key, tự động fallback trả về danh sách gốc.
    """
    if not settings.COHERE_API_KEY:
        log.warning("Reranker: Không tìm thấy COHERE_API_KEY. Bỏ qua Rerank (Fallback mode).")
        return candidates
    
    if not candidates:
        return []

    limit = settings.AGENT_RERANKER_CANDIDATES_LIMIT
    input_candidates = candidates[:limit]

    rerank_model = model or settings.AGENT_RERANKER_MODEL
    rerank_top_n = top_n or settings.AGENT_RERANKER_TOP_N

    # Sử dụng Cohere Rerank API v2 theo đặc tả mới nhất
    url = "https://api.cohere.com/v2/rerank"
    headers = {
        "Authorization": f"Bearer {settings.COHERE_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    
    payload = {
        "model": rerank_model,
        "query": query,
        "documents": [c.get("content", "") for c in input_candidates],
        "top_n": min(rerank_top_n, len(input_candidates))
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=8.0)
            
            if response.status_code != 200:
                log.error(f"Reranker: Cohere API v2 trả về mã lỗi {response.status_code}: {response.text}")
                return candidates  # Fallback
                
            results = response.json().get("results", [])
            
            reranked_candidates = []
            for item in results:
                idx = item["index"]
                relevance_score = float(item["relevance_score"])
                
                candidate = input_candidates[idx].copy()
                candidate["similarity"] = round(relevance_score, 4)
                candidate["final_score"] = round(relevance_score, 4)
                candidate["retrieval_method"] = "cohere-rerank-v2"
                
                reranked_candidates.append(candidate)
                
            log.info(f"Reranker: Đã Rerank thành công {len(reranked_candidates)} chunks bằng Cohere v2 API.")
            return reranked_candidates

    except httpx.HTTPError as http_err:
        log.error(f"Reranker: Lỗi kết nối HTTP tới Cohere API v2: {http_err}")
    except asyncio.TimeoutError:
        log.error("Reranker: Gọi Cohere API v2 bị quá hạn (Timeout).")
    except Exception as e:
        log.error(f"Reranker: Lỗi không xác định khi thực hiện rerank: {e}")
        
    return candidates