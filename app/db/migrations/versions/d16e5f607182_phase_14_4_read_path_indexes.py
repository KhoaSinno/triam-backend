"""phase 14.4 read path indexes

Revision ID: d16e5f607182
Revises: c15d3e4f5061
Create Date: 2026-06-15
"""

from typing import Sequence, Union

from alembic import op

revision: str = "d16e5f607182"
down_revision: Union[str, None] = "c15d3e4f5061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create index if not exists ix_books_user_created_at on books (user_id, created_at desc, id desc)")
    op.execute(
        """
        create index if not exists ix_reading_plans_book_status_updated
        on reading_plans (book_id, status, updated_at desc, created_at desc)
        """
    )
    op.execute(
        """
        create index if not exists ix_learning_unit_progress_user_book_mode_updated
        on learning_unit_progress (user_id, book_id, mode, updated_at desc)
        """
    )
    op.execute(
        """
        create index if not exists ix_learning_unit_progress_user_book_mode_activity
        on learning_unit_progress (user_id, book_id, mode, last_activity_at desc)
        where last_activity_at is not null
        """
    )
    op.execute(
        """
        create index if not exists ix_spaced_review_items_user_book_mode_status_due
        on spaced_review_items (user_id, book_id, mode, status, due_at)
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_user_local_date_scheduled
        on reading_plan_sessions (user_id, local_date, scheduled_at, session_index)
        where status <> 'cancelled'
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_user_book_mode_scheduled
        on reading_plan_sessions (user_id, book_id, mode, scheduled_at, session_index)
        where status <> 'cancelled'
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_overdue_user_status_scheduled
        on reading_plan_sessions (user_id, status, scheduled_at)
        where status in ('scheduled', 'due', 'in_progress')
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_due_reminder_status_scheduled
        on reading_plan_sessions (status, scheduled_at)
        where status in ('scheduled', 'due')
        """
    )


def downgrade() -> None:
    op.execute("drop index if exists ix_rps_due_reminder_status_scheduled")
    op.execute("drop index if exists ix_rps_overdue_user_status_scheduled")
    op.execute("drop index if exists ix_rps_user_book_mode_scheduled")
    op.execute("drop index if exists ix_rps_user_local_date_scheduled")
    op.execute("drop index if exists ix_spaced_review_items_user_book_mode_status_due")
    op.execute("drop index if exists ix_learning_unit_progress_user_book_mode_activity")
    op.execute("drop index if exists ix_learning_unit_progress_user_book_mode_updated")
    op.execute("drop index if exists ix_reading_plans_book_status_updated")
    op.execute("drop index if exists ix_books_user_created_at")
