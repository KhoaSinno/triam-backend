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
    NotificationOutbox,
)
from app.core.constant import BookStatus, PlanMode, PlanStatus, LearningProgressStatus, NotificationStatus
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

        # Lấy session_id vừa được tạo
        sessions_before = session.exec(select(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id)).all()
        assert len(sessions_before) > 0
        test_session_id = sessions_before[0].id

        # Tạo tin nhắn nhắc nhở PENDING trong outbox
        outbox_item = NotificationOutbox(
            user_id=user_id,
            type="plan_reminder",
            status=NotificationStatus.PENDING,
            payload={},
            due_at=datetime.now(timezone.utc),
            idempotency_key=f"plan-session-reminder:{test_session_id}",
        )
        session.add(outbox_item)

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

        db_outbox_before = session.exec(select(NotificationOutbox).where(NotificationOutbox.idempotency_key == f"plan-session-reminder:{test_session_id}")).first()
        assert db_outbox_before is not None

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

        # Tin nhắn PENDING trong outbox của session cũ phải bị xóa
        db_outbox_after = session.exec(select(NotificationOutbox).where(NotificationOutbox.idempotency_key == f"plan-session-reminder:{test_session_id}")).first()
        assert db_outbox_after is None

        # Lịch học cũ phải được dọn dẹp và nạp lại lịch bắt đầu từ bài 1 (Unit 1)
        sessions_after = session.exec(select(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id)).all()
        assert len(sessions_after) > 0
        
        # Dọn dẹp dữ liệu test tránh ảnh hưởng môi trường
        session.execute(delete(BookLearningState).where(BookLearningState.book_id == book_id))
        session.execute(delete(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id))
        session.execute(delete(ReadingPlanSessionUnit).where(ReadingPlanSessionUnit.plan_id == plan_id))
        session.execute(delete(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id))
        session.execute(delete(ReadingPlan).where(ReadingPlan.id == plan_id))
        session.execute(delete(LearningUnit).where(LearningUnit.book_id == book_id))
        session.execute(delete(Book).where(Book.id == book_id))
        session.execute(delete(NotificationOutbox).where(NotificationOutbox.user_id == user_id))
        session.commit()
