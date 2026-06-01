import base64

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Sử dụng book ID có sẵn trong môi trường test/local.
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"


def test_full_study_context_flow():
    """
    Kiểm thử tích hợp (Integration Test) luồng Study Context từ A-Z.
    1. Tạo mới Context
    2. Gắn sách (Document) vào Context
    3. Tạo luồng chat (Thread) trong Context
    4. Lấy token LiveKit và xác nhận Agent Dispatch Metadata được đính kèm đúng.
    5. Dọn dẹp dữ liệu (Xóa Context).
    """
    # 1. Tạo Context
    create_ctx_res = client.post("/api/v1/study-contexts", json={"title": "Test Context Ôn Thi"})
    assert create_ctx_res.status_code == 200, "Không thể tạo Study Context"
    context = create_ctx_res.json()
    assert "id" in context
    context_id = context["id"]

    try:
        # 2. Gắn Document (Sách) vào Context
        doc_res = client.post(f"/api/v1/study-contexts/{context_id}/documents", json={"book_id": MOCK_BOOK_ID})
        # Nếu MOCK_BOOK_ID thực sự có trong DB thì sẽ trả 200, nếu không sẽ 404 (Book not found).
        if doc_res.status_code == 200:
            link = doc_res.json()
            assert link["context_id"] == context_id
            assert link["book_id"] == MOCK_BOOK_ID
        elif doc_res.status_code == 404:
            print(f"\n⚠️ Warning: Sách {MOCK_BOOK_ID} không tồn tại trong DB, bỏ qua check link document.")
        else:
            pytest.fail(f"Lỗi không mong muốn khi thêm document: {doc_res.text}")

        # 3. Tạo luồng Chat (Thread)
        thread_res = client.post(f"/api/v1/study-contexts/{context_id}/threads", json={"title": "Thread Test Toán"})
        assert thread_res.status_code == 200, "Không thể tạo Chat Thread"
        thread = thread_res.json()
        assert "id" in thread
        assert thread["context_id"] == context_id
        thread_id = thread["id"]

        # 4. Kiểm tra cấp quyền LiveKit Token
        token_res = client.get(f"/api/v1/live-token/thread/{thread_id}")
        assert token_res.status_code == 200, "Không thể lấy LiveKit Token"
        token_data = token_res.json()
        assert "token" in token_data
        assert "room_name" in token_data

        jwt_token = token_data["token"]

        # Decode phần payload của JWT Token
        payload_part = jwt_token.split(".")[1]
        # Pad base64 missing '='
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_payload = base64.b64decode(payload_part).decode("utf-8")

        # Kiểm tra xem chuỗi JSON JWT có chứa thread_id và context_id không
        # (chứng tỏ metadata được truyền xuống Agent thành công)
        assert thread_id in decoded_payload, "JWT Token không chứa thông tin thread_id"
        assert context_id in decoded_payload, "JWT Token không chứa thông tin context_id"

        print("\n✅ Luồng Study Context -> Thread -> LiveKit Token hoạt động hoàn hảo!")

    finally:
        # 5. Dọn dẹp (Xóa Context và các Threads/Documents cascade theo)
        delete_res = client.delete(f"/api/v1/study-contexts/{context_id}")
        assert delete_res.status_code == 200, "Xóa Study Context thất bại sau khi test"
