import uuid
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.db.database import engine
from app.models.db_models import (
    AdminUser,
    Book,
    BookSection,
    BookSectionKnowledge,
    LearningUnit,
    LearningUnitSegment,
    LearningUnitSource
)

@pytest.fixture
def test_db_session():
    with Session(engine) as session:
        yield session


def test_select_book_from_library_flow(auth_as, test_db_session: Session):
    admin_user_id = uuid.uuid4()
    regular_user_id = uuid.uuid4()
    
    # 1. Khởi tạo một sách mẫu của hệ thống nhưng chưa được chia sẻ (is_shared=False)
    shared_book = Book(
        user_id=admin_user_id,
        title="Sách Giáo Khoa Mẫu",
        author="Tác Giả Mẫu",
        file_url="https://supabase.storage/raw_books/sample.pdf",
        document_type="pdf",
        total_sections=1,
        total_units=1,
        status="ready",
        is_shared=False
    )
    test_db_session.add(shared_book)
    
    # Tạo quyền Admin cho admin_user_id
    admin_record = AdminUser(user_id=admin_user_id, role="admin")
    test_db_session.add(admin_record)
    test_db_session.commit()
    test_db_session.refresh(shared_book)

    # Thêm metadata cho sách mẫu
    section = BookSection(
        book_id=shared_book.id,
        title="Chương Một",
        level=1,
        section_index=0,
        path="0",
        text_content="Nội dung chương một mẫu.",
        text_char_count=24
    )
    test_db_session.add(section)
    test_db_session.commit()
    test_db_session.refresh(section)

    knowledge = BookSectionKnowledge(
        book_id=shared_book.id,
        section_id=section.id,
        chunk_index=0,
        content="Nội dung chương một mẫu.",
        search_text="Chương Một: Nội dung chương một mẫu.",
        content_hash="mock_hash_123",
        embedding_model="text-embedding-3-small",
        embedding_version="v1",
        char_count=24,
        embedding=[0.1] * 1536
    )
    test_db_session.add(knowledge)

    unit = LearningUnit(
        user_id=admin_user_id,
        book_id=shared_book.id,
        mode="full",
        unit_index=0,
        title="Bài Học Đầu Tiên",
        unit_type="full_chapter",
        status="ready",
        main_segment_count=1,
        estimated_tokens=50,
        source_text_char_count=24
    )
    test_db_session.add(unit)
    test_db_session.commit()
    test_db_session.refresh(unit)

    source = LearningUnitSource(
        learning_unit_id=unit.id,
        section_id=section.id,
        source_order=0
    )
    segment = LearningUnitSegment(
        learning_unit_id=unit.id,
        segment_index=0,
        audio_url="https://supabase.storage/audios/sample_audio.mp3",
        text_content="Nội dung chương một mẫu.",
        duration_ms=5000
    )
    test_db_session.add(source)
    test_db_session.add(segment)
    test_db_session.commit()

    client = TestClient(app)
    cloned_book_id = None

    try:
        # Bước 2. Đăng nhập với User thường và kiểm tra: Sách chưa được chia sẻ không được hiển thị
        auth_as(regular_user_id)
        
        # Test API GET /books/library -> Trống hoặc không chứa sách này
        lib_response = client.get("/api/v1/books/library")
        if lib_response.status_code != 200:
            print("ERROR RESPONSE:", lib_response.json())
        assert lib_response.status_code == 200
        titles = [item["title"] for item in lib_response.json()]
        assert "Sách Giáo Khoa Mẫu" not in titles
        
        # Test API POST /books/{shared_book_id}/select -> Báo lỗi vì chưa share
        select_fail_response = client.post(f"/api/v1/books/{shared_book.id}/select")
        assert select_fail_response.status_code == 400
        assert "chưa được chia sẻ" in select_fail_response.json()["detail"]

        # Bước 3. Đăng nhập Admin để chuyển đổi trạng thái sách mẫu sang dùng chung
        auth_as(admin_user_id)
        share_response = client.patch(f"/api/v1/admin/books/{shared_book.id}/share")
        assert share_response.status_code == 200
        assert share_response.json()["is_shared"] is True

        # Bước 4. Đăng nhập lại với User thường và kiểm tra: Sách đã xuất hiện và có thể chọn
        auth_as(regular_user_id)
        
        # Check library
        lib_response = client.get("/api/v1/books/library")
        assert lib_response.status_code == 200
        titles = [item["title"] for item in lib_response.json()]
        assert "Sách Giáo Khoa Mẫu" in titles

        # Chọn sách
        select_response = client.post(f"/api/v1/books/{shared_book.id}/select")
        assert select_response.status_code == 200
        cloned_book_data = select_response.json()
        assert cloned_book_data["parent_shared_id"] == str(shared_book.id)
        assert cloned_book_data["status"] == "ready"
        
        cloned_book_id = uuid.UUID(cloned_book_data["id"])
        
        # Verify user_id via database lookup
        test_db_session.expire_all()
        db_cloned = test_db_session.get(Book, cloned_book_id)
        assert db_cloned is not None
        assert db_cloned.user_id == regular_user_id

        # Bước 5. Kiểm tra tính chính xác của dữ liệu được nhân bản trong DB
        # Kiểm tra BookSection đã clone
        cloned_sec = test_db_session.exec(select(BookSection).where(BookSection.book_id == cloned_book_id)).first()
        assert cloned_sec is not None
        assert cloned_sec.title == "Chương Một"
        assert cloned_sec.id != section.id

        # Kiểm tra BookSectionKnowledge đã clone
        cloned_kn = test_db_session.exec(select(BookSectionKnowledge).where(BookSectionKnowledge.book_id == cloned_book_id)).first()
        assert cloned_kn is not None
        assert list(cloned_kn.embedding) == [0.1] * 1536
        
        # Kiểm tra LearningUnit đã clone
        cloned_unit = test_db_session.exec(select(LearningUnit).where(LearningUnit.book_id == cloned_book_id)).first()
        assert cloned_unit is not None
        assert cloned_unit.user_id == regular_user_id
        
        # Kiểm tra LearningUnitSegment đã clone
        cloned_seg = test_db_session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id == cloned_unit.id)).first()
        assert cloned_seg is not None
        assert cloned_seg.audio_url == "https://supabase.storage/audios/sample_audio.mp3"

        # Bước 6. Kiểm tra việc tạo ReadingPlan trên sách clone (Phải chạy thành công ngay lập tức mà không xóa audio cũ)
        plan_response = client.post("/api/v1/generate-plan", json={
            "book_id": str(cloned_book_id),
            "mode": "full",
            "pace": 1,
            "schedule_config": ["Mon"],
            "reminder_time": "08:00",
            "activate": True
        })
        assert plan_response.status_code == 200
        assert "Kế hoạch học tập đã được tạo" in plan_response.json()["message"]

        # Kiểm tra trong DB: ReadingPlan đã được tạo thành công
        from app.models.db_models import ReadingPlan
        db_plan = test_db_session.exec(select(ReadingPlan).where(ReadingPlan.book_id == cloned_book_id)).first()
        assert db_plan is not None
        assert db_plan.pace == 1
        assert db_plan.status == "active"

        # Bước 7. Kiểm tra xóa an toàn sách clone ("Cắt đuôi" file vật lý)
        delete_response = client.delete(f"/api/v1/books/{cloned_book_id}")
        assert delete_response.status_code == 200
        
        # Đảm bảo sách clone trong DB đã biến mất hoàn toàn nhờ CASCADE
        test_db_session.expire_all()
        assert test_db_session.get(Book, cloned_book_id) is None
        
        # Đảm bảo sách mẫu gốc của hệ thống vẫn an toàn không bị ảnh hưởng
        assert test_db_session.get(Book, shared_book.id) is not None
        assert test_db_session.get(BookSection, section.id) is not None

    finally:
        # Dọn dẹp dữ liệu kiểm thử
        test_db_session.delete(admin_record)
        cleanup_db_records(test_db_session, shared_book.id)
        if cloned_book_id:
            cleanup_db_records(test_db_session, cloned_book_id)
        test_db_session.commit()


def cleanup_db_records(session: Session, book_id: uuid.UUID):
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


def test_admin_upload_processing_and_auto_share(auth_as, test_db_session: Session, monkeypatch):
    from app.models.db_models import ProcessingJob
    from app.core.constant import ProcessingJobStatus, BookStatus, PlanMode
    from app.services.workers.book_pipeline import _set_book_status

    # Mock Celery apply_async to avoid actual Redis/Celery queue connections
    calls = []
    def fake_apply_async(*args, **kwargs):
        calls.append(kwargs)
    monkeypatch.setattr("app.services.admin_service.process_book_task.apply_async", fake_apply_async)

    admin_user_id = uuid.uuid4()
    regular_user_id = uuid.uuid4()

    # 1. Khởi tạo sách mẫu nháp của Admin
    admin_book = Book(
        user_id=admin_user_id,
        title="Sách Khoa Học Thường Thức",
        author="Tác Giả Khoa Học",
        file_url="https://supabase.storage/raw_books/science.pdf",
        document_type="pdf",
        total_sections=1,
        total_units=0,
        status="draft",
        is_shared=False
    )
    test_db_session.add(admin_book)

    # Thêm BookSection cho sách
    section = BookSection(
        book_id=admin_book.id,
        title="Chương Một Khoa Học",
        level=1,
        section_index=0,
        path="0",
        text_content="Kiến thức khoa học vũ trụ bao la.",
        text_char_count=32
    )
    test_db_session.add(section)

    # Thêm BookSectionKnowledge cho sách
    knowledge = BookSectionKnowledge(
        book_id=admin_book.id,
        section_id=section.id,
        chunk_index=0,
        content="Kiến thức khoa học vũ trụ bao la.",
        search_text="Chương Một Khoa Học: Kiến thức khoa học vũ trụ bao la.",
        content_hash="science_hash_123",
        embedding_model="text-embedding-3-small",
        embedding_version="v1",
        char_count=32,
        embedding=[0.2] * 1536
    )
    test_db_session.add(knowledge)

    # Đăng ký quyền Admin
    admin_record = AdminUser(user_id=admin_user_id, role="admin")
    test_db_session.add(admin_record)
    test_db_session.commit()
    test_db_session.refresh(admin_book)
    test_db_session.refresh(section)

    client = TestClient(app)

    try:
        # Đăng nhập Admin
        auth_as(admin_user_id)

        # Trigger processing cho FULL mode với auto-share
        response_full = client.post(
            f"/api/v1/admin/books/{admin_book.id}/process",
            params={"mode": "full", "is_shared": True}
        )
        assert response_full.status_code == 200
        job_full_data = response_full.json()["job"]
        job_full_id = uuid.UUID(job_full_data["id"])

        # Trigger processing cho PARETO mode với auto-share
        response_pareto = client.post(
            f"/api/v1/admin/books/{admin_book.id}/process",
            params={"mode": "pareto", "is_shared": True}
        )
        assert response_pareto.status_code == 200
        job_pareto_data = response_pareto.json()["job"]
        job_pareto_id = uuid.UUID(job_pareto_data["id"])

        # Kiểm tra trạng thái sách trong DB: Phải chuyển sang processing và is_shared=True
        test_db_session.expire_all()
        db_book = test_db_session.get(Book, admin_book.id)
        assert db_book.status == "processing"
        assert db_book.is_shared is True

        # Lúc này, mặc dù is_shared=True nhưng status vẫn là processing,
        # nên User thường chưa thể thấy sách này trong Thư viện
        auth_as(regular_user_id)
        lib_response = client.get("/api/v1/books/library")
        assert lib_response.status_code == 200
        titles = [item["title"] for item in lib_response.json()]
        assert "Sách Khoa Học Thường Thức" not in titles

        # Giả lập Celery Worker 1: Hoàn thành Job FULL mode
        # Cập nhật trạng thái job FULL thành ready (thành công)
        test_db_session.expire_all()
        job_full = test_db_session.get(ProcessingJob, job_full_id)
        job_full.status = ProcessingJobStatus.READY
        test_db_session.add(job_full)
        test_db_session.commit()

        # Gọi set_book_status khi hoàn thành job FULL
        _set_book_status(admin_book.id, BookStatus.READY, current_job_id=job_full_id)

        # Do Job PARETO vẫn đang processing/queued, book status phải là PARTIAL_READY
        test_db_session.expire_all()
        db_book_after_full = test_db_session.get(Book, admin_book.id)
        assert db_book_after_full.status == "partial_ready"

        # User thường vẫn CHƯA thấy sách trong library
        lib_response2 = client.get("/api/v1/books/library")
        titles2 = [item["title"] for item in lib_response2.json()]
        assert "Sách Khoa Học Thường Thức" not in titles2

        # Giả lập Celery Worker 2: Hoàn thành Job PARETO mode
        # Cập nhật trạng thái job PARETO thành ready (thành công)
        job_pareto = test_db_session.get(ProcessingJob, job_pareto_id)
        job_pareto.status = ProcessingJobStatus.READY
        test_db_session.add(job_pareto)
        test_db_session.commit()

        # Gọi set_book_status khi hoàn thành job PARETO
        _set_book_status(admin_book.id, BookStatus.READY, current_job_id=job_pareto_id)

        # Không còn job nào chạy, book status phải chuyển sang READY
        test_db_session.expire_all()
        db_book_after_all = test_db_session.get(Book, admin_book.id)
        assert db_book_after_all.status == "ready"

        # Bây giờ sách đã READY và is_shared=True -> User thường PHẢI thấy sách trong library
        lib_response3 = client.get("/api/v1/books/library")
        titles3 = [item["title"] for item in lib_response3.json()]
        assert "Sách Khoa Học Thường Thức" in titles3

    finally:
        # Dọn dẹp dữ liệu
        test_db_session.delete(admin_record)
        cleanup_db_records(test_db_session, admin_book.id)
        test_db_session.commit()

