import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects import postgresql

from app.core.constant import PlanMode
from app.models.db_models import BookLearningState
from app.repositories.book_learning_state_repo import upsert_book_learning_state


class _ScalarResult:
    def __init__(self, value):
        self._value = value

    def scalar_one(self):
        return self._value


class _Session:
    def __init__(self, state):
        self.state = state
        self.statement = None
        self.commit_count = 0

    def execute(self, statement):
        self.statement = statement
        return _ScalarResult(self.state.id)

    def commit(self):
        self.commit_count += 1

    def get(self, model, state_id):
        assert model is BookLearningState
        assert state_id == self.state.id
        return self.state


def test_upsert_book_learning_state_uses_atomic_postgres_conflict_update():
    state = BookLearningState(id=uuid.uuid4(), user_id=uuid.uuid4(), book_id=uuid.uuid4(), mode=PlanMode.FULL)
    session = _Session(state)

    result = upsert_book_learning_state(
        session,
        user_id=state.user_id,
        book_id=state.book_id,
        mode=PlanMode.FULL,
        status="in_progress",
        book_progress_percent=20,
        completed_units=1,
        playable_units=5,
        last_learning_unit_id=uuid.uuid4(),
        last_segment_id=42,
        last_segment_index=3,
        position_ms=1200,
        started_at=datetime.now(timezone.utc),
        last_activity_at=datetime.now(timezone.utc),
        completed_at=None,
    )

    compiled = str(session.statement.compile(dialect=postgresql.dialect()))
    assert "ON CONFLICT ON CONSTRAINT uq_book_learning_state_user_book_mode DO UPDATE" in compiled
    assert "coalesce(book_learning_states.started_at, excluded.started_at)" in compiled
    assert "coalesce(book_learning_states.completed_at, excluded.completed_at)" in compiled
    assert session.commit_count == 1
    assert result is state
