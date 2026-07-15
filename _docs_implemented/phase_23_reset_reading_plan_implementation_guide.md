# Phase 23: Reset Reading Plan Implementation Guide

Hướng dẫn này trình bày chi tiết cách thiết lập và hiện thực tính năng **Reset Reading Plan (Đặt lại kế hoạch học tập từ đầu)** cho người dùng theo chuẩn kiến trúc phân lớp Clean Architecture của hệ thống TRIAM.

---

## 1. Mục tiêu Nghiệp vụ (Business Goal)
* Cung cấp nút bấm hoặc tùy chọn trên giao diện cho phép người học bắt đầu lại từ đầu một cuốn sách đã hoàn thành hoặc đang học dở dang.
* Xóa bỏ hoàn toàn tiến độ ghi nhận trong bảng `LearningUnitProgress` và các buổi học cũ (`ReadingPlanSession`, `ReadingPlanSessionUnit`) để đưa tiến trình sách về $0\%$.
* Giải phóng cơ sở dữ liệu và tự động tạo lại lịch học mới tinh dựa trên cấu hình slot và pace hiện tại.

---

## 2. Thiết Kế Phân Lớp (Layered Architecture Design)

Tuân thủ nguyên tắc: **Thao tác truy vấn cơ sở dữ liệu (SQL/ORM) phải sống ở tầng Repository, tầng Service chỉ sở hữu business logic điều phối nghiệp vụ và quản trị giao dịch (Transaction).**

```text
FE Client: POST /api/v1/books/{book_id}/reset
    │
    ▼
FastAPI Router: reset_plan (audiobooks.py)
    │
    ▼
Service Layer: reset_reading_plan (audiobook_service.py)
    │ (Điều phối nghiệp vụ và Transaction commit)
    ├─► learning_progress_repo.delete_book_progress(...)
    ├─► book_learning_state_repo.reset_book_learning_state(...)
    ├─► reading_plan_session_repo.delete_sessions_for_plan(...)
    ├─► Reset trạng thái ReadingPlan
    └─► ensure_future_sessions_for_plan(...)
```

---

## 3. Mã Nguồn Chi Tiết Cần Hiện Thực (Code Specifications)

### Bước 3.1: Hiện thực tầng Repository

#### 1. Bổ sung hàm xóa tiến độ trong [learning_progress_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/learning_progress_repo.py)
```python
from sqlmodel import delete

def delete_book_progress(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ tiến độ các bài học của user đối với sách và mode nhất định."""
    session.execute(
        delete(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
        )
    )
```

#### 2. Bổ sung hàm reset tiến độ tổng quan trong [book_learning_state_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/book_learning_state_repo.py)
```python
def reset_book_learning_state(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Đặt lại trạng thái tiến độ tổng quan của sách về ban đầu."""
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if state:
        state.status = "not_started"
        state.book_progress_percent = 0
        state.completed_units = 0
        state.playable_units = 0
        state.last_learning_unit_id = None
        state.last_segment_id = None
        state.last_segment_index = None
        state.position_ms = 0
        state.started_at = None
        state.completed_at = None
        state.updated_at = datetime.now(timezone.utc)
        session.add(state)
```

#### 3. Bổ sung hàm xóa lịch học trong [reading_plan_session_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/reading_plan_session_repo.py)
```python
from sqlmodel import delete

def delete_sessions_for_plan(session: Session, *, plan_id: uuid.UUID) -> None:
    """Xóa toàn bộ các buổi học và chi tiết buổi học của kế hoạch học tập."""
    session.execute(
        delete(ReadingPlanSessionUnit)
        .where(ReadingPlanSessionUnit.plan_id == plan_id)
    )
    session.execute(
        delete(ReadingPlanSession)
        .where(ReadingPlanSession.plan_id == plan_id)
    )
```

#### 4. Bổ sung hàm xóa thẻ ôn tập trong [spaced_review_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/spaced_review_repo.py)
```python
from sqlmodel import delete

def delete_spaced_review_items(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ các thẻ ôn tập ngắt quãng của user đối với sách và mode nhất định."""
    session.execute(
        delete(SpacedReviewItem)
        .where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    )
```

#### 5. Bổ sung hàm xóa tin nhắn nhắc nhở trong hàng đợi tại [notification_outbox_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/notification_outbox_repo.py)
```python
from sqlmodel import delete
from app.core.constant import NotificationStatus

def delete_pending_outbox_by_keys(session: Session, *, keys: list[str]) -> None:
    """Xóa toàn bộ các thông báo đang chờ gửi (status = PENDING) có idempotency_key thuộc danh sách."""
    if not keys:
        return
    session.execute(
        delete(NotificationOutbox)
        .where(NotificationOutbox.status == NotificationStatus.PENDING)
        .where(NotificationOutbox.idempotency_key.in_(keys))
    )
```

---

### Bước 3.2: Hiện thực tầng Service trong [audiobook_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/audiobook_service.py)

Bổ sung hàm `reset_reading_plan` gọi các Repository helpers và làm chủ transaction commit:

```python
from app.repositories.learning_progress_repo import delete_book_progress
from app.repositories.book_learning_state_repo import reset_book_learning_state
from app.repositories.reading_plan_session_repo import delete_sessions_for_plan
from app.repositories.spaced_review_repo import delete_spaced_review_items
from app.repositories.notification_outbox_repo import delete_pending_outbox_by_keys

def reset_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """
    Đặt lại toàn bộ tiến độ học tập và lịch biểu của cuốn sách từ đầu cho chế độ học hiện tại.
    """
    # 1. Xác thực sách và kế hoạch học tập hiện có
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    
    plan = _active_plan(session, book_id, user_id)
    now = datetime.now(timezone.utc)
    mode = PlanMode(plan.mode)

    # 2. Thu thập danh sách ID của các buổi học (sessions) cũ
    sessions = session.exec(
        select(ReadingPlanSession.id).where(ReadingPlanSession.plan_id == plan.id)
    ).all()
    session_ids = [str(sid) for sid in sessions]

    # 3. Thu thập danh sách ID của các thẻ ôn tập (spaced review items) cũ
    review_items = session.exec(
        select(SpacedReviewItem.id).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    ).all()
    review_ids = [str(rid) for rid in review_items]

    # 4. Tạo danh sách các idempotency_key tương ứng trong hàng đợi thông báo để xóa
    keys_to_delete = []
    for sid in session_ids:
        keys_to_delete.append(f"plan-session-reminder:{sid}")
        keys_to_delete.append(f"plan-session-missed:{sid}")
    for rid in review_ids:
        keys_to_delete.append(f"spaced-review:{rid}")

    # 5. Gọi các Repo xóa sạch dữ liệu tiến trình & lịch học
    delete_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    reset_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_spaced_review_items(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_sessions_for_plan(session, plan_id=plan.id)

    # 6. Hủy toàn bộ các thông báo đẩy PENDING còn sót lại trong Outbox
    delete_pending_outbox_by_keys(session, keys=keys_to_delete)
    
    # Commit trung gian để đồng bộ xóa CSDL tránh xung đột khóa ngoại
    session.flush()

    # 6. Đặt lại trạng thái kế hoạch học tập ban đầu
    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = now
    plan.paused_at = None
    plan.completed_at = None
    plan.updated_at = now
    session.add(plan)
    session.flush()

    # 7. Tự động xếp lịch mới bắt đầu từ Bài học thứ nhất
    ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)
    
    session.commit()
    return {
        "message": "Đã đặt lại kế hoạch học tập từ đầu thành công.",
        **_reading_plan_to_dict(session, plan)
    }
```

---

### Bước 3.3: Định nghĩa Endpoint trong [audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py)

Khai báo route mới trong file router [audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py):

```python
from app.services.audiobook_service import reset_reading_plan

@router.post("/books/{book_id}/reset", response_model=ReadingPlanResponse)
def reset_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """
    Đặt lại kế hoạch học tập của cuốn sách từ đầu.
    Xóa sạch tiến độ học tập cũ của user và sinh lại các buổi học từ bài 1.
    """
    return reset_reading_plan(session, book_id, current_user.sub)
```

---

## 4. Hướng Dẫn Kiểm Thử Tự Động (Pytest)

Tạo tệp kiểm thử tích hợp [test_reset_reading_plan.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/test_reset_reading_plan.py):

```python
# tests/services/test_reset_reading_plan.py
import uuid
from datetime import datetime, timezone
from sqlmodel import Session, select, delete

from app.db.database import engine
from app.models.db_models import (
    Book,
    LearningUnit,
    LearningUnitProgress,
    ReadingPlan,
    ReadingPlanSession,
    ReadingPlanSessionUnit,
    ReadingPlanScheduleSlot,
    BookLearningState,
)
from app.core.constant import BookStatus, PlanMode, PlanStatus, LearningProgressStatus
from app.services.audiobook_service import reset_reading_plan
from app.services.reading_plan_session_service import ensure_future_sessions_for_plan

def test_reset_reading_plan_success():
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()
    plan_id = uuid.uuid4()

    with Session(engine) as session:
        # 1. Seed dữ liệu test cô lập
        book = Book(
            id=book_id,
            user_id=user_id,
            title="Sách test reset",
            status=BookStatus.READY.value,
            total_sections=1,
            total_units=2,
        )
        session.add(book)
        session.flush()

        unit1 = LearningUnit(id=uuid.uuid4(), user_id=user_id, book_id=book_id, mode=PlanMode.PARETO, unit_index=0, title="Unit 1", unit_type="main")
        unit2 = LearningUnit(id=uuid.uuid4(), user_id=user_id, book_id=book_id, mode=PlanMode.PARETO, unit_index=1, title="Unit 2", unit_type="main")
        session.add(unit1)
        session.add(unit2)
        session.flush()

        plan = ReadingPlan(
            id=plan_id,
            book_id=book_id,
            mode=PlanMode.PARETO.value,
            pace=1,
            status=PlanStatus.ACTIVE.value,
            reminder_time="19:00",
        )
        session.add(plan)
        session.flush()

        # Cấu hình slot học Thứ 2 (weekday=0)
        slot = ReadingPlanScheduleSlot(
            plan_id=plan_id,
            book_id=book_id,
            user_id=user_id,
            weekday=0,
            reminder_time="19:00",
            timezone="Asia/Ho_Chi_Minh",
            is_active=True,
        )
        session.add(slot)
        session.flush()
        session.commit()

        # Sinh lịch học ban đầu
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id)
        session.commit()

        # Tạo tiến độ học hoàn thành cho Unit 1
        progress = LearningUnitProgress(
            user_id=user_id,
            book_id=book_id,
            learning_unit_id=unit1.id,
            mode=PlanMode.PARETO,
            status=LearningProgressStatus.COMPLETED,
        )
        session.add(progress)

        # Tạo trạng thái tiến độ sách (completed, 100%)
        state = BookLearningState(
            user_id=user_id,
            book_id=book_id,
            mode=PlanMode.PARETO,
            status="completed",
            book_progress_percent=100,
        )
        session.add(state)
        session.commit()

        # Xác thực trạng thái trước khi reset
        db_progress = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.user_id == user_id)).all()
        assert len(db_progress) == 1

        # 2. Gọi hàm reset nghiệp vụ
        result = reset_reading_plan(session, book_id=book_id, user_id=user_id)
        assert result["message"] == "Đã đặt lại kế hoạch học tập từ đầu thành công."

        # 3. Assert các thay đổi trong DB sau khi reset
        # Trạng thái tiến độ thực tế phải bị xóa sạch (về 0)
        db_progress_after = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.user_id == user_id)).all()
        assert len(db_progress_after) == 0

        # BookLearningState phải reset về not_started và 0%
        db_state = session.exec(select(BookLearningState).where(BookLearningState.user_id == user_id, BookLearningState.book_id == book_id, BookLearningState.mode == PlanMode.PARETO)).first()
        assert db_state is not None
        assert db_state.status == "not_started"
        assert db_state.book_progress_percent == 0

        # Lịch học cũ phải được dọn dẹp và nạp lại lịch bắt đầu từ bài 1 (Unit 1)
        sessions = session.exec(select(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id)).all()
        assert len(sessions) > 0
        
        # Dọn dẹp dữ liệu test tránh ảnh hưởng môi trường
        session.execute(delete(BookLearningState).where(BookLearningState.book_id == book_id))
        session.execute(delete(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id))
        session.execute(delete(ReadingPlanSessionUnit).where(ReadingPlanSessionUnit.plan_id == plan_id))
        session.execute(delete(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id))
        session.execute(delete(ReadingPlan).where(ReadingPlan.id == plan_id))
        session.execute(delete(LearningUnit).where(LearningUnit.book_id == book_id))
        session.execute(delete(Book).where(Book.id == book_id))
        session.commit()
```

Lệnh thực thi chạy test cô lập:
```powershell
uv run pytest tests/services/test_reset_reading_plan.py -v
```
