import pytest
import uuid
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select

from app.db.database import engine
from app.core.constant import PlanMode, ReviewItemStatus, LearningProgressStatus
from app.models.db_models import SpacedReviewItem, Book, LearningUnit, LearningUnitProgress
from app.services.spaced_review_service import (
    create_spaced_reviews_after_unit_completion,
    SPACED_REVIEW_INTERVALS,
)
from app.services.review_service import complete_review_item, skip_review_item


def _setup_test_data(session: Session):
    user_id = uuid.uuid4()
    
    book = Book(
        user_id=user_id,
        title="Test Spaced Review Book",
        status="ready",
        is_shared=False,
    )
    session.add(book)
    session.flush()

    unit = LearningUnit(
        book_id=book.id,
        user_id=user_id,
        title="Test Unit 1",
        unit_index=0,
        mode="pareto",
        unit_type="pareto",
        status="READY",
        review_text="Test summary",
    )
    session.add(unit)
    session.flush()

    progress = LearningUnitProgress(
        user_id=user_id,
        book_id=book.id,
        learning_unit_id=unit.id,
        mode="pareto",
        status="completed",
        completed_at=datetime.now(timezone.utc),
        max_progress_percent=100,
        elapsed_seconds=120,
    )
    session.add(progress)
    session.flush()
    
    return user_id, book, unit, progress


def test_spaced_review_generation_after_success() -> None:
    with Session(engine) as session:
        user_id, book, unit, progress = _setup_test_data(session)

        # Trigger
        created = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary",
            completed_at=progress.completed_at,
            source_unit_progress_id=progress.id,
        )

        # Verify - Chỉ tạo 1 bản ghi duy nhất cho chu kỳ đầu
        assert len(created) == 1
        item = created[0]
        assert item.user_id == user_id
        assert item.book_id == book.id
        assert item.learning_unit_id == unit.id
        assert item.mode == PlanMode.PARETO
        assert item.interval_days == 1
        assert item.sequence_index == 0
        assert item.status == ReviewItemStatus.PENDING
        assert item.review_text_snapshot == "Test summary"
        assert item.anchor_completed_at == progress.completed_at
        assert item.source_unit_progress_id == progress.id
        assert item.due_at == progress.completed_at + timedelta(days=1)
        
        session.rollback()


def test_spaced_review_avoid_duplicate_during_active_chain() -> None:
    with Session(engine) as session:
        user_id, book, unit, progress = _setup_test_data(session)

        first_round = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary",
            completed_at=progress.completed_at,
            source_unit_progress_id=progress.id,
        )
        assert len(first_round) == 1

        # Trigger second time -> should NOT create duplicate items since active items exist
        second_round = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary 2",
            completed_at=progress.completed_at,
            source_unit_progress_id=progress.id,
        )
        assert len(second_round) == 0
        
        session.rollback()


def test_spaced_review_re_anchor_flow() -> None:
    with Session(engine) as session:
        user_id, book, unit, progress = _setup_test_data(session)
        progress.completed_at = datetime.now(timezone.utc) - timedelta(days=5)
        session.add(progress)
        session.flush()

        # Trigger first batch
        first_round = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary",
            completed_at=progress.completed_at,
            source_unit_progress_id=progress.id,
        )
        assert len(first_round) == 1

        # Re-anchor second round
        second_round = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary 2",
            completed_at=datetime.now(timezone.utc),
            source_unit_progress_id=progress.id,
        )
        assert len(second_round) == 0
        
        session.rollback()


def test_spaced_review_dynamic_chain_transition() -> None:
    with Session(engine) as session:
        user_id, book, unit, progress = _setup_test_data(session)

        # 1. Tạo chu kỳ đầu tiên (ngày 1)
        created = create_spaced_reviews_after_unit_completion(
            session,
            user_id=user_id,
            book_id=book.id,
            learning_unit_id=unit.id,
            mode=PlanMode.PARETO,
            review_text="Test summary",
            completed_at=progress.completed_at,
            source_unit_progress_id=progress.id,
        )
        assert len(created) == 1
        item_1 = created[0]
        assert item_1.sequence_index == 0
        assert item_1.interval_days == 1

        # 2. Hoàn thành chu kỳ đầu tiên -> Nên tự động sinh chu kỳ tiếp theo (ngày 3)
        complete_res = complete_review_item(session, user_id=user_id, review_item_id=item_1.id)
        assert complete_res.status == ReviewItemStatus.COMPLETED
        
        # Truy vấn xem bản ghi mới đã được tạo chưa
        reviews = session.exec(
            select(SpacedReviewItem)
            .where(SpacedReviewItem.learning_unit_id == unit.id)
            .order_by(SpacedReviewItem.sequence_index)
        ).all()
        
        assert len(reviews) == 2
        assert reviews[0].status == ReviewItemStatus.COMPLETED
        assert reviews[1].status == ReviewItemStatus.PENDING
        assert reviews[1].sequence_index == 1
        assert reviews[1].interval_days == 3

        # 3. Bỏ qua (Skip) chu kỳ tiếp theo -> Nên tự động sinh chu kỳ tiếp theo (ngày 7)
        item_2 = reviews[1]
        skip_res = skip_review_item(session, user_id=user_id, review_item_id=item_2.id)
        assert skip_res.status == ReviewItemStatus.SKIPPED

        reviews_updated = session.exec(
            select(SpacedReviewItem)
            .where(SpacedReviewItem.learning_unit_id == unit.id)
            .order_by(SpacedReviewItem.sequence_index)
        ).all()
        
        assert len(reviews_updated) == 3
        assert reviews_updated[0].status == ReviewItemStatus.COMPLETED
        assert reviews_updated[1].status == ReviewItemStatus.SKIPPED
        assert reviews_updated[2].status == ReviewItemStatus.PENDING
        assert reviews_updated[2].sequence_index == 2
        assert reviews_updated[2].interval_days == 7
        
        session.rollback()
