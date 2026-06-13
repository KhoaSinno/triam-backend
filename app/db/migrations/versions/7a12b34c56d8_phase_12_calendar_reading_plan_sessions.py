"""phase 12 calendar reading plan sessions

Revision ID: 7a12b34c56d8
Revises: 2f6b7c8d9e01
Create Date: 2026-06-11
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "7a12b34c56d8"
down_revision: Union[str, None] = "2f6b7c8d9e01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.create_table(
        "reading_plan_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("session_index", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("local_date", sa.Text(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("timezone", sa.Text(), server_default="Asia/Ho_Chi_Minh", nullable=False),
        sa.Column("status", sa.Text(), server_default="scheduled", nullable=False),
        sa.Column("completed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("skipped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("missed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_id", "session_index", name="uq_reading_plan_sessions_plan_index"),
    )
    op.create_index("ix_reading_plan_sessions_user_id", "reading_plan_sessions", ["user_id"])
    op.create_index("ix_reading_plan_sessions_plan_id", "reading_plan_sessions", ["plan_id"])
    op.create_index("ix_reading_plan_sessions_book_id", "reading_plan_sessions", ["book_id"])
    op.create_index("ix_reading_plan_sessions_mode", "reading_plan_sessions", ["mode"])
    op.create_index("ix_reading_plan_sessions_scheduled_at", "reading_plan_sessions", ["scheduled_at"])
    op.create_index("ix_reading_plan_sessions_local_date", "reading_plan_sessions", ["local_date"])
    op.create_index("ix_reading_plan_sessions_status", "reading_plan_sessions", ["status"])
    op.create_index("ix_reading_plan_sessions_completed_at", "reading_plan_sessions", ["completed_at"])
    op.create_index("ix_reading_plan_sessions_user_status", "reading_plan_sessions", ["user_id", "status"])
    op.create_index("ix_reading_plan_sessions_book_mode", "reading_plan_sessions", ["book_id", "mode"])
    op.create_index("ix_reading_plan_sessions_plan_status", "reading_plan_sessions", ["plan_id", "status"])
    op.create_index(
        "uq_reading_plan_sessions_user_scheduled_active",
        "reading_plan_sessions",
        ["user_id", "scheduled_at"],
        unique=True,
        postgresql_where=sa.text("status != 'cancelled'"),
    )

    op.create_table(
        "reading_plan_session_units",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("unit_order", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), server_default="pending", nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["reading_plan_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_id", "learning_unit_id", name="uq_reading_plan_session_units_plan_unit"),
        sa.UniqueConstraint("session_id", "unit_order", name="uq_reading_plan_session_units_session_order"),
    )
    op.create_index("ix_reading_plan_session_units_session_id", "reading_plan_session_units", ["session_id"])
    op.create_index("ix_reading_plan_session_units_plan_id", "reading_plan_session_units", ["plan_id"])
    op.create_index("ix_reading_plan_session_units_book_id", "reading_plan_session_units", ["book_id"])
    op.create_index("ix_reading_plan_session_units_learning_unit_id", "reading_plan_session_units", ["learning_unit_id"])
    op.create_index("ix_reading_plan_session_units_status", "reading_plan_session_units", ["status"])
    op.create_index("ix_reading_plan_session_units_completed_at", "reading_plan_session_units", ["completed_at"])
    op.create_index("ix_reading_plan_session_units_session_status", "reading_plan_session_units", ["session_id", "status"])
    op.create_index("ix_reading_plan_session_units_book_unit", "reading_plan_session_units", ["book_id", "learning_unit_id"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_session_units_book_unit", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_session_status", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_completed_at", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_status", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_learning_unit_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_book_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_plan_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_session_id", table_name="reading_plan_session_units")
    op.drop_table("reading_plan_session_units")

    op.drop_index("uq_reading_plan_sessions_user_scheduled_active", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_plan_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_book_mode", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_user_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_completed_at", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_local_date", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_scheduled_at", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_mode", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_book_id", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_plan_id", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_user_id", table_name="reading_plan_sessions")
    op.drop_table("reading_plan_sessions")
