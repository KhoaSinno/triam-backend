"""
tests/test_api_flow.py
======================
Test đầy đủ luồng API cho hệ thống Triam Audiobook:

LUỒNG 1 (FULL):   upload PDF → generate-plan (full)  → poll status → get details
LUỒNG 2 (PARETO): tái sử dụng book_id từ Luồng 1     → generate-plan (pareto) (book khác)
LUỒNG 3 (SWITCH): dùng book đã gen full               → switch-mode sang pareto → get details

Cách chạy:
    # Đảm bảo server đang chạy trước:
    # bash start.sh   hoặc   uv run uvicorn app.main:app --port 8000 --reload

    # Test nhanh (không cần background task):
    uv run pytest tests/test_api_flow.py -v -s -k "not slow"

    # Test đầy đủ tất cả luồng (mất 5-20 phút):
    uv run pytest tests/test_api_flow.py -v -s -m slow

    # Trỏ vào server khác:
    TEST_BASE_URL=http://localhost:8080 uv run pytest tests/test_api_flow.py -v -s

Biến môi trường:
    TEST_BASE_URL=http://localhost:8000   (mặc định)
    TEST_PDF_PATH=tests/sample.pdf        (file PDF mẫu — nếu không có sẽ dùng PDF giả)
"""

import os
import socket
import time
import uuid

import pytest
import httpx

# ─── Cấu hình ────────────────────────────────────────────────────────────────

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")
API_V1 = f"{BASE_URL}/api/v1"
SAMPLE_PDF = os.getenv("TEST_PDF_PATH", "tests/sample.pdf")

# Timeout tối đa để poll trạng thái book (giây)
POLL_TIMEOUT = 600   # 10 phút — background task có thể mất nhiều thời gian
POLL_INTERVAL = 10   # kiểm tra mỗi 10 giây


# ─── Check server availability ───────────────────────────────────────────────

def _is_server_running(url: str) -> bool:
    """Kiểm tra server có đang chạy không."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 80
        with socket.create_connection((host, port), timeout=3):
            return True
    except (OSError, ConnectionRefusedError):
        return False


# Skip toàn bộ module nếu server không chạy
pytestmark = pytest.mark.skipif(
    not _is_server_running(BASE_URL),
    reason=f"Server không chạy tại {BASE_URL}. Chạy server trước: bash start.sh",
)

# ─── Helpers ─────────────────────────────────────────────────────────────────


def _upload_pdf(client: httpx.Client, pdf_path: str) -> dict:
    """Upload file PDF và trả về response JSON."""
    with open(pdf_path, "rb") as f:
        resp = client.post(
            f"{API_V1}/upload",
            files={"file": (os.path.basename(pdf_path), f, "application/pdf")},
            timeout=60,
        )
    assert resp.status_code == 200, f"Upload thất bại: {resp.status_code} | {resp.text}"
    data = resp.json()
    assert "book_id" in data, "Response thiếu book_id"
    assert "outline" in data, "Response thiếu outline"
    print(f"\n  ✅ Upload OK | book_id={data['book_id']} | chapters={data['total_chapters']}")
    return data


def _generate_plan(client: httpx.Client, book_id: str, mode: str) -> dict:
    """Gửi generate-plan và trả về response JSON."""
    payload = {
        "book_id": book_id,
        "mode": mode,
        "pace": 3,
        "schedule_config": ["Mon", "Wed", "Fri"],
    }
    resp = client.post(f"{API_V1}/generate-plan", json=payload, timeout=30)
    assert resp.status_code == 200, f"generate-plan thất bại: {resp.status_code} | {resp.text}"
    data = resp.json()
    print(f"  ✅ generate-plan OK | mode={mode} | message={data.get('message', '')[:60]}")
    return data


def _poll_until_ready(client: httpx.Client, book_id: str, mode: str) -> dict:
    """
    Poll GET /books/{book_id}/details cho đến khi book_status == READY
    hoặc hết POLL_TIMEOUT.
    """
    deadline = time.time() + POLL_TIMEOUT
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        resp = client.get(f"{API_V1}/books/{book_id}/details", timeout=30)
        assert resp.status_code == 200, f"get-details thất bại: {resp.status_code} | {resp.text}"
        data = resp.json()
        status = data.get("book_status")
        print(f"  ⏳ Poll #{attempt} | status={status}")
        if status == "READY":
            print(f"  ✅ Book READY sau {attempt} lần poll")
            return data
        if status == "ERROR":
            pytest.fail(f"Book chuyển sang ERROR: {data}")
        time.sleep(POLL_INTERVAL)

    pytest.fail(f"Timeout sau {POLL_TIMEOUT}s — book chưa READY")


def _poll_until_segments_ready(client: httpx.Client, book_id: str, mode: str) -> dict:
    """
    Poll dành riêng cho switch-mode: đợi cho đến khi chapter đầu tiên
    có ít nhất 1 segment của mode đích.
    (Dùng sau switch-mode vì book_status không thay đổi khi switch.)
    """
    deadline = time.time() + POLL_TIMEOUT
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        resp = client.get(f"{API_V1}/books/{book_id}/details", timeout=30)
        assert resp.status_code == 200, f"get-details thất bại: {resp.status_code} | {resp.text}"
        data = resp.json()
        chapters = data.get("chapters", [])
        seg_count = len(chapters[0].get("chapter_segments", [])) if chapters else 0
        print(f"  ⏳ Poll #{attempt} | mode={mode} | segments={seg_count}")
        if seg_count > 0:
            print(f"  ✅ Segments của mode={mode} đã sẵn sàng sau {attempt} lần poll")
            return data
        time.sleep(POLL_INTERVAL)

    pytest.fail(f"Timeout sau {POLL_TIMEOUT}s — segments mode={mode} chưa được gen")



def _get_details(client: httpx.Client, book_id: str) -> dict:
    resp = client.get(f"{API_V1}/books/{book_id}/details", timeout=30)
    assert resp.status_code == 200, f"get-details thất bại: {resp.status_code} | {resp.text}"
    return resp.json()


def _switch_mode(client: httpx.Client, book_id: str, mode: str) -> dict:
    resp = client.post(
        f"{API_V1}/books/{book_id}/switch-mode",
        json={"mode": mode},
        timeout=30,
    )
    assert resp.status_code == 200, f"switch-mode thất bại: {resp.status_code} | {resp.text}"
    data = resp.json()
    print(f"  ✅ switch-mode OK | mode={mode} | needs_generation={data.get('needs_generation')}")
    return data


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def client():
    """HTTP client dùng chung cho toàn bộ test suite."""
    with httpx.Client(timeout=60) as c:
        yield c

# sample_pdf fixture được define trong conftest.py (tạo PDF thật bằng fpdf2)



# ─── Test Cases ──────────────────────────────────────────────────────────────


class TestUploadEndpoint:
    """Kiểm tra Endpoint POST /upload"""

    def test_upload_success(self, client, sample_pdf):
        """Upload PDF hợp lệ phải trả về book_id và outline."""
        data = _upload_pdf(client, sample_pdf)
        assert uuid.UUID(data["book_id"])  # phải là UUID hợp lệ
        assert isinstance(data["total_chapters"], int)
        assert isinstance(data["outline"], list)

    def test_upload_wrong_type(self, client, tmp_path):
        """Upload file không phải PDF phải trả về 400."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("hello")
        with open(str(txt_file), "rb") as f:
            resp = client.post(
                f"{API_V1}/upload",
                files={"file": ("test.txt", f, "text/plain")},
                timeout=30,
            )
        assert resp.status_code == 400, f"Phải trả 400 nhưng nhận được {resp.status_code}"
        print(f"\n  ✅ Upload sai type → 400 (đúng)")


class TestGeneratePlanEndpoint:
    """Kiểm tra Endpoint POST /generate-plan"""

    def test_generate_plan_full(self, client, sample_pdf):
        """Tạo plan với mode 'full' phải thành công."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        result = _generate_plan(client, book_id, "full")
        assert result.get("mode") == "full"

    def test_generate_plan_pareto_mode_uppercase(self, client, sample_pdf):
        """Flutter gửi 'PARETO_MODE' phải được normalize về 'pareto'."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        result = _generate_plan(client, book_id, "PARETO_MODE")
        assert result.get("mode") == "pareto", f"Mode không được normalize: {result.get('mode')}"

    def test_generate_plan_full_mode_uppercase(self, client, sample_pdf):
        """Flutter gửi 'FULL_MODE' phải được normalize về 'full'."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        result = _generate_plan(client, book_id, "FULL_MODE")
        assert result.get("mode") == "full", f"Mode không được normalize: {result.get('mode')}"

    def test_generate_plan_invalid_mode(self, client, sample_pdf):
        """Mode không hợp lệ phải trả về 400."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        resp = client.post(
            f"{API_V1}/generate-plan",
            json={"book_id": book_id, "mode": "INVALID_MODE", "pace": 3, "schedule_config": ["Mon"]},
            timeout=30,
        )
        assert resp.status_code == 400, f"Phải trả 400 nhưng nhận được {resp.status_code}"
        print(f"\n  ✅ Mode không hợp lệ → 400 (đúng)")

    def test_generate_plan_book_not_found(self, client):
        """book_id không tồn tại phải trả về 404."""
        fake_id = str(uuid.uuid4())
        resp = client.post(
            f"{API_V1}/generate-plan",
            json={"book_id": fake_id, "mode": "full", "pace": 3, "schedule_config": ["Mon"]},
            timeout=30,
        )
        assert resp.status_code == 404, f"Phải trả 404 nhưng nhận được {resp.status_code}"
        print(f"\n  ✅ Book không tồn tại → 404 (đúng)")


class TestGetDetailsEndpoint:
    """Kiểm tra Endpoint GET /books/{book_id}/details"""

    def test_get_details_not_found(self, client):
        """book_id không tồn tại phải trả về 404."""
        fake_id = str(uuid.uuid4())
        resp = client.get(f"{API_V1}/books/{fake_id}/details", timeout=30)
        assert resp.status_code == 404
        print(f"\n  ✅ Details sách không tồn tại → 404 (đúng)")

    def test_get_details_structure(self, client, sample_pdf):
        """Response phải có đủ fields book_status, total_chapters, chapters."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        _generate_plan(client, book_id, "full")
        data = _get_details(client, book_id)
        assert "book_status" in data
        assert "total_chapters" in data
        assert "chapters" in data
        print(f"\n  ✅ Cấu trúc details hợp lệ")


class TestSwitchModeEndpoint:
    """Kiểm tra Endpoint POST /books/{book_id}/switch-mode"""

    def test_switch_invalid_mode(self, client, sample_pdf):
        """Mode không hợp lệ phải trả về 400."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        _generate_plan(client, book_id, "full")
        resp = client.post(
            f"{API_V1}/books/{book_id}/switch-mode",
            json={"mode": "INVALID"},
            timeout=30,
        )
        assert resp.status_code == 400
        print(f"\n  ✅ switch-mode với mode không hợp lệ → 400 (đúng)")

    def test_switch_no_plan(self, client, sample_pdf):
        """Switch mode khi chưa có ReadingPlan phải trả về 404."""
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        # KHÔNG gọi generate-plan, switch ngay
        resp = client.post(
            f"{API_V1}/books/{book_id}/switch-mode",
            json={"mode": "pareto"},
            timeout=30,
        )
        assert resp.status_code == 404
        print(f"\n  ✅ switch-mode khi chưa có plan → 404 (đúng)")


class TestFullFlowFull:
    """
    LUỒNG ĐẦY ĐỦ: Upload → generate-plan (full) → poll READY → verify details
    ⚠️  Test này mất nhiều thời gian vì phải chờ Background Task hoàn thành.
    Chạy riêng: pytest tests/test_api_flow.py::TestFullFlowFull -v -s
    """

    @pytest.mark.slow
    def test_full_mode_flow(self, client, sample_pdf):
        print("\n\n=== LUỒNG 1: FULL MODE ===")
        
        # Bước 1: Upload PDF
        print("📤 Bước 1: Upload PDF...")
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]

        # Bước 2: Tạo plan với mode full
        print("📋 Bước 2: Tạo generate-plan (full)...")
        plan_resp = _generate_plan(client, book_id, "full")
        assert plan_resp.get("mode") == "full"

        # Bước 3: Poll cho đến khi READY
        print("⏳ Bước 3: Đợi background processing...")
        details = _poll_until_ready(client, book_id, "full")

        # Bước 4: Kiểm tra cấu trúc và dữ liệu
        print("🔍 Bước 4: Kiểm tra kết quả...")
        assert details["book_status"] == "READY"
        chapters = details["chapters"]
        assert len(chapters) > 0, "Phải có ít nhất 1 chapter"

        # Kiểm tra chapter đầu tiên có segments và review
        first_chap = chapters[0]
        segments = first_chap.get("chapter_segments", [])
        assert len(segments) > 0, "Chapter đầu tiên phải có ít nhất 1 segment"

        # Kiểm tra mode của segment
        for seg in segments:
            assert seg.get("mode") == "full", f"Segment phải có mode='full', nhận được: {seg.get('mode')}"

        print(f"  ✅ Chapter 0: {len(segments)} segments, mode=full")
        print(f"  ✅ review_text: {'CÓ' if first_chap.get('review_text') else 'KHÔNG'}")
        print(f"  ✅ review_audio_url: {'CÓ' if first_chap.get('review_audio_url') else 'KHÔNG'}")
        print("\n✅ LUỒNG 1 (FULL MODE) HOÀN THÀNH!")


class TestFullFlowPareto:
    """
    LUỒNG ĐẦY ĐỦ: Upload → generate-plan (pareto) → poll READY → verify details
    """

    @pytest.mark.slow
    def test_pareto_mode_flow(self, client, sample_pdf):
        print("\n\n=== LUỒNG 2: PARETO MODE ===")

        print("📤 Bước 1: Upload PDF...")
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]

        print("📋 Bước 2: Tạo generate-plan (PARETO_MODE - uppercase)...")
        plan_resp = _generate_plan(client, book_id, "PARETO_MODE")
        assert plan_resp.get("mode") == "pareto", "Phải được normalize về 'pareto'"

        print("⏳ Bước 3: Đợi background processing...")
        details = _poll_until_ready(client, book_id, "pareto")

        print("🔍 Bước 4: Kiểm tra kết quả...")
        assert details["book_status"] == "READY"
        chapters = details["chapters"]
        assert len(chapters) > 0

        first_chap = chapters[0]
        segments = first_chap.get("chapter_segments", [])
        assert len(segments) > 0

        for seg in segments:
            assert seg.get("mode") == "pareto", f"Segment phải có mode='pareto', nhận được: {seg.get('mode')}"

        print(f"  ✅ Chapter 0: {len(segments)} segments, mode=pareto")
        print("\n✅ LUỒNG 2 (PARETO MODE) HOÀN THÀNH!")


class TestFullFlowSwitchMode:
    """
    LUỒNG SWITCH: Upload → gen full → poll READY → switch sang pareto
                  → poll READY → verify details pareto
    Đây là test case phức tạp nhất, kiểm tra tính năng dual-mode.
    """

    @pytest.mark.slow
    def test_switch_mode_full_to_pareto(self, client, sample_pdf):
        print("\n\n=== LUỒNG 3: SWITCH FULL → PARETO ===")

        # PHASE 1: Gen Full
        print("📤 Bước 1: Upload PDF...")
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]

        print("📋 Bước 2: Tạo generate-plan (full)...")
        _generate_plan(client, book_id, "full")

        print("⏳ Bước 3: Đợi full mode READY...")
        details_full = _poll_until_ready(client, book_id, "full")
        assert details_full["book_status"] == "READY"

        # Kiểm tra segments của full mode
        chapters = details_full["chapters"]
        first_chap = chapters[0]
        full_segments = first_chap.get("chapter_segments", [])
        assert all(s.get("mode") == "full" for s in full_segments), "Tất cả segments phải là 'full'"
        print(f"  ✅ Full mode: {len(full_segments)} segments cho chapter 0")

        # PHASE 2: Switch sang Pareto
        print("\n🔄 Bước 4: Switch sang pareto mode...")
        switch_resp = _switch_mode(client, book_id, "pareto")
        needs_gen = switch_resp.get("needs_generation")
        assert needs_gen is True, "Pareto chưa có dữ liệu → needs_generation phải là True"

        # PHASE 3: Poll cho đến khi pareto segments xuất hiện
        # Dùng _poll_until_segments_ready vì book_status không thay đổi khi switch-mode
        print("⏳ Bước 5: Đợi pareto segments được gen...")
        details_pareto = _poll_until_segments_ready(client, book_id, "pareto")

        # Kiểm tra details bây giờ trả về pareto data
        chapters_pareto = details_pareto["chapters"]
        first_chap_pareto = chapters_pareto[0]
        pareto_segments = first_chap_pareto.get("chapter_segments", [])
        assert len(pareto_segments) > 0, "Pareto phải có segments sau khi gen"
        assert all(s.get("mode") == "pareto" for s in pareto_segments), "Tất cả segments phải là 'pareto'"
        print(f"  ✅ Pareto mode: {len(pareto_segments)} segments cho chapter 0")
        print(f"  ✅ review_text pareto: {'CÓ' if first_chap_pareto.get('review_text') else 'KHÔNG'}")

        # PHASE 4: Switch lại Full — phải instant (không gen lại)
        print("\n🔄 Bước 6: Switch ngược lại full mode...")
        switch_back = _switch_mode(client, book_id, "full")
        assert switch_back.get("needs_generation") is False, "Full đã có → needs_generation phải là False"

        # Xác nhận details trả về full data
        details_back_full = _get_details(client, book_id)
        chapters_back_full = details_back_full["chapters"]
        segments_back = chapters_back_full[0].get("chapter_segments", [])
        assert all(s.get("mode") == "full" for s in segments_back), "Phải quay về full segments"
        print(f"  ✅ Quay về full: {len(segments_back)} segments, tất cả mode='full'")

        print("\n✅ LUỒNG 3 (SWITCH MODE FULL ↔ PARETO) HOÀN THÀNH!")


    @pytest.mark.slow
    def test_switch_already_has_mode(self, client, sample_pdf):
        """Switch sang mode đã có sẵn (same mode) phải trả needs_generation=False."""
        print("\n\n=== TEST: Switch sang mode đã có (same mode) ===")
        
        upload = _upload_pdf(client, sample_pdf)
        book_id = upload["book_id"]
        _generate_plan(client, book_id, "full")
        
        print("⏳ Đợi full mode READY...")
        _poll_until_ready(client, book_id, "full")

        # Switch sang full (đã là full) → phải instant
        print("🔄 Switch sang full (mode đã có sẵn)...")
        switch_resp = _switch_mode(client, book_id, "full")
        assert switch_resp.get("needs_generation") is False, \
            "Switch sang mode đã có → needs_generation phải False"
        print("  ✅ Switch same mode → needs_generation=False (đúng)")
