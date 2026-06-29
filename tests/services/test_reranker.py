import pytest
from unittest.mock import AsyncMock, patch
import httpx

from app.core.config import settings
from app.services.agent_grounding.reranker import rerank_candidates


@pytest.mark.asyncio
async def test_rerank_candidates_success():
    """Kiểm tra luồng Rerank thành công khi API Cohere v2 phản hồi 200."""
    candidates = [
        {"id": "chunk_1", "content": "Toán rời rạc học về mệnh đề và logic.", "similarity": 0.5},
        {"id": "chunk_2", "content": "Hệ thống tưới nước tự động cho ban công.", "similarity": 0.3},
    ]
    query = "biến mệnh đề là gì"

    # Định nghĩa dữ liệu giả lập trả về từ Cohere v2 API
    mock_cohere_response = {
        "id": "mock-response-id-123",
        "results": [
            {"index": 0, "relevance_score": 0.95},
            {"index": 1, "relevance_score": 0.12},
        ]
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        # Mock đối tượng phản hồi HTTP của httpx
        mock_response = httpx.Response(200, json=mock_cohere_response)
        mock_post.return_value = mock_response

        # Chạy hàm test với API Key đã mock
        with patch.object(settings, "COHERE_API_KEY", "mock_key_123"):
            result = await rerank_candidates(query, candidates)

            assert len(result) == 2
            # Chunks phải được cập nhật relevance score và giữ đúng cấu trúc
            assert result[0]["id"] == "chunk_1"
            assert result[0]["similarity"] == 0.95
            assert result[0]["retrieval_method"] == "cohere-rerank-v2"
            assert result[1]["similarity"] == 0.12


@pytest.mark.asyncio
async def test_rerank_candidates_fallback_on_network_error():
    """Kiểm tra cơ chế Fallback tự động trả về danh sách thô nếu API Cohere v2 lỗi."""
    candidates = [
        {"id": "chunk_1", "content": "Mệnh đề logic học.", "similarity": 0.5},
        {"id": "chunk_2", "content": "Hệ thống tưới nước.", "similarity": 0.3},
    ]
    query = "biến mệnh đề"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Giả lập ném ra lỗi Timeout
        mock_post.side_effect = httpx.TimeoutException("Connection timed out")

        with patch.object(settings, "COHERE_API_KEY", "mock_key_123"):
            # Chạy hàm, ngoại lệ phải được bắt và danh sách gốc được trả về
            result = await rerank_candidates(query, candidates)
            
            assert len(result) == 2
            assert result == candidates  # Trả về nguyên mẫu không sửa đổi
            assert result[0]["similarity"] == 0.5  # Giữ nguyên điểm heuristics cũ
