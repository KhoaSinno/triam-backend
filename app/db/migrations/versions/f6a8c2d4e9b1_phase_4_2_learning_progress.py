"""phase 4.2 learning progress

Revision ID: f6a8c2d4e9b1
Revises: e4f7a9c2d1b0
Create Date: 2026-05-25
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f6a8c2d4e9b1"
down_revision: Union[str, None] = "e4f7a9c2d1b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


learning_progress_status = postgresql.ENUM(
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    name="learningprogressstatus",
    create_type=False,
)
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    learning_progress_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "reading_plan_schedule_slots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reading_plan_schedule_slots_user_id", "reading_plan_schedule_slots", ["user_id"])
    op.create_index("ix_reading_plan_schedule_slots_plan_id", "reading_plan_schedule_slots", ["plan_id"])
    op.create_index("ix_reading_plan_schedule_slots_book_id", "reading_plan_schedule_slots", ["book_id"])
    op.create_index("ix_reading_plan_schedule_slots_is_active", "reading_plan_schedule_slots", ["is_active"])
    op.create_index("ix_reading_plan_schedule_slots_user_active", "reading_plan_schedule_slots", ["user_id", "is_active"])
    op.create_index(
        "uq_active_plan_slot_user_weekday_time",
        "reading_plan_schedule_slots",
        ["user_id", "weekday", "reminder_time"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )

    op.create_table(
        "chapter_learning_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("current_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=False),
        sa.Column("position_ms", sa.Integer(), nullable=False),
        sa.Column("listened_ms", sa.Integer(), nullable=False),
        sa.Column("total_duration_ms", sa.Integer(), nullable=False),
        sa.Column("progress_percent", sa.Integer(), nullable=False),
        sa.Column("max_progress_percent", sa.Integer(), nullable=False),
        sa.Column("status", learning_progress_status, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["current_segment_id"], ["chapter_segments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "mode", name="uq_learning_progress_user_chapter_mode"),
    )
    op.create_index("ix_chapter_learning_progress_user_id", "chapter_learning_progress", ["user_id"])
    op.create_index("ix_chapter_learning_progress_book_id", "chapter_learning_progress", ["book_id"])
    op.create_index("ix_chapter_learning_progress_chapter_id", "chapter_learning_progress", ["chapter_id"])
    op.create_index("ix_chapter_learning_progress_status", "chapter_learning_progress", ["status"])
    op.create_index("ix_chapter_learning_progress_last_activity_at", "chapter_learning_progress", ["last_activity_at"])
    op.create_index("ix_chapter_learning_progress_completed_at", "chapter_learning_progress", ["completed_at"])
    op.create_index("ix_learning_progress_user_book_mode", "chapter_learning_progress", ["user_id", "book_id", "mode"])
    op.create_index("ix_learning_progress_user_book_status", "chapter_learning_progress", ["user_id", "book_id", "status"])
    op.create_index("ix_learning_progress_user_book_activity", "chapter_learning_progress", ["user_id", "book_id", "last_activity_at"])

    op.add_column("spaced_review_items", sa.Column("anchor_completed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_progress_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("notified_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("spaced_review_items", sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(
        "fk_spaced_review_items_source_progress_id",
        "spaced_review_items",
        "chapter_learning_progress",
        ["source_progress_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_spaced_review_items_anchor_completed_at", "spaced_review_items", ["anchor_completed_at"])
    op.create_index("ix_spaced_review_items_source_progress_id", "spaced_review_items", ["source_progress_id"])

    op.execute("UPDATE spaced_review_items SET status = 'CANCELLED' WHERE source_progress_id IS NULL")
    op.drop_constraint("uq_review_user_chapter_mode_interval", "spaced_review_items", type_="unique")
    op.create_index(
        "uq_review_active_user_chapter_interval",
        "spaced_review_items",
        ["user_id", "chapter_id", "interval_days"],
        unique=True,
        postgresql_where=sa.text("status != 'CANCELLED'"),
    )


def downgrade() -> None:
    op.drop_index("uq_review_active_user_chapter_interval", table_name="spaced_review_items")
    op.create_unique_constraint(
        "uq_review_user_chapter_mode_interval",
        "spaced_review_items",
        ["user_id", "chapter_id", "mode", "interval_days"],
    )
    op.drop_index("ix_spaced_review_items_source_progress_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_anchor_completed_at", table_name="spaced_review_items")
    op.drop_constraint("fk_spaced_review_items_source_progress_id", "spaced_review_items", type_="foreignkey")
    op.drop_column("spaced_review_items", "last_reviewed_at")
    op.drop_column("spaced_review_items", "notified_at")
    op.drop_column("spaced_review_items", "source_progress_id")
    op.drop_column("spaced_review_items", "anchor_completed_at")

    op.drop_index("ix_learning_progress_user_book_activity", table_name="chapter_learning_progress")
    op.drop_index("ix_learning_progress_user_book_status", table_name="chapter_learning_progress")
    op.drop_index("ix_learning_progress_user_book_mode", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_completed_at", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_last_activity_at", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_status", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_chapter_id", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_book_id", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_user_id", table_name="chapter_learning_progress")
    op.drop_table("chapter_learning_progress")

    op.drop_index("uq_active_plan_slot_user_weekday_time", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_user_active", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_is_active", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_book_id", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_plan_id", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_user_id", table_name="reading_plan_schedule_slots")
    op.drop_table("reading_plan_schedule_slots")

    learning_progress_status.drop(op.get_bind(), checkfirst=True)
