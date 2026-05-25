"""phase 4.1 in app notifications

Revision ID: e4f7a9c2d1b0
Revises: d7a2f4c9b8e1
Create Date: 2026-05-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e4f7a9c2d1b0"
down_revision: Union[str, None] = "d7a2f4c9b8e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


notification_type = postgresql.ENUM(
    "PLAN_REMINDER",
    "CONTENT_READY",
    "SPACED_REVIEW_DUE",
    name="notificationtype",
    create_type=False,
)
notification_channel = postgresql.ENUM("IN_APP", name="notificationchannel", create_type=False)
notification_status = postgresql.ENUM(
    "PENDING",
    "PROCESSING",
    "SENT",
    "FAILED",
    "CANCELLED",
    "SKIPPED",
    name="notificationstatus",
    create_type=False,
)
review_item_status = postgresql.ENUM(
    "PENDING",
    "DUE",
    "COMPLETED",
    "SKIPPED",
    "CANCELLED",
    name="reviewitemstatus",
    create_type=False,
)
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    notification_type.create(op.get_bind(), checkfirst=True)
    notification_channel.create(op.get_bind(), checkfirst=True)
    notification_status.create(op.get_bind(), checkfirst=True)
    review_item_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "notification_settings",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.Column("reminders_enabled", sa.Boolean(), nullable=False),
        sa.Column("spaced_review_enabled", sa.Boolean(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("quiet_hours_start", sa.Text(), nullable=False),
        sa.Column("quiet_hours_end", sa.Text(), nullable=False),
        sa.Column("daily_cap", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "spaced_review_items",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("interval_days", sa.Integer(), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", review_item_status, nullable=False),
        sa.Column("review_text_snapshot", sa.Text(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "mode", "interval_days", name="uq_review_user_chapter_mode_interval"),
    )
    op.create_index("ix_spaced_review_items_user_id", "spaced_review_items", ["user_id"])
    op.create_index("ix_spaced_review_items_book_id", "spaced_review_items", ["book_id"])
    op.create_index("ix_spaced_review_items_chapter_id", "spaced_review_items", ["chapter_id"])
    op.create_index("ix_spaced_review_items_due_at", "spaced_review_items", ["due_at"])
    op.create_index("ix_spaced_review_items_status", "spaced_review_items", ["status"])
    op.create_index("ix_spaced_review_items_status_due_at", "spaced_review_items", ["status", "due_at"])

    op.create_table(
        "notification_outbox",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("type", notification_type, nullable=False),
        sa.Column("channel", notification_channel, nullable=False),
        sa.Column("status", notification_status, nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_by", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key", name="uq_notification_outbox_idempotency_key"),
    )
    op.create_index("ix_notification_outbox_user_id", "notification_outbox", ["user_id"])
    op.create_index("ix_notification_outbox_type", "notification_outbox", ["type"])
    op.create_index("ix_notification_outbox_channel", "notification_outbox", ["channel"])
    op.create_index("ix_notification_outbox_status", "notification_outbox", ["status"])
    op.create_index("ix_notification_outbox_due_at", "notification_outbox", ["due_at"])
    op.create_index("ix_notification_outbox_next_retry_at", "notification_outbox", ["next_retry_at"])
    op.create_index("ix_notification_outbox_status_due_at", "notification_outbox", ["status", "due_at"])
    op.create_index("ix_notification_outbox_status_next_retry_at", "notification_outbox", ["status", "next_retry_at"])

    op.create_table(
        "user_notifications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("outbox_id", sa.UUID(), nullable=True),
        sa.Column("type", notification_type, nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=True),
        sa.Column("action_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["outbox_id"], ["notification_outbox.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("outbox_id", name="uq_user_notifications_outbox_id"),
    )
    op.create_index("ix_user_notifications_user_id", "user_notifications", ["user_id"])
    op.create_index("ix_user_notifications_outbox_id", "user_notifications", ["outbox_id"])
    op.create_index("ix_user_notifications_type", "user_notifications", ["type"])
    op.create_index("ix_user_notifications_user_created_at", "user_notifications", ["user_id", "created_at"])
    op.create_index("ix_user_notifications_user_read_at", "user_notifications", ["user_id", "read_at"])


def downgrade() -> None:
    op.drop_index("ix_user_notifications_user_read_at", table_name="user_notifications")
    op.drop_index("ix_user_notifications_user_created_at", table_name="user_notifications")
    op.drop_index("ix_user_notifications_type", table_name="user_notifications")
    op.drop_index("ix_user_notifications_outbox_id", table_name="user_notifications")
    op.drop_index("ix_user_notifications_user_id", table_name="user_notifications")
    op.drop_table("user_notifications")

    op.drop_index("ix_notification_outbox_status_next_retry_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_status_due_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_next_retry_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_due_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_status", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_channel", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_type", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_user_id", table_name="notification_outbox")
    op.drop_table("notification_outbox")

    op.drop_index("ix_spaced_review_items_status_due_at", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_status", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_due_at", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_chapter_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_book_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_user_id", table_name="spaced_review_items")
    op.drop_table("spaced_review_items")

    op.drop_table("notification_settings")

    review_item_status.drop(op.get_bind(), checkfirst=True)
    notification_status.drop(op.get_bind(), checkfirst=True)
    notification_channel.drop(op.get_bind(), checkfirst=True)
    notification_type.drop(op.get_bind(), checkfirst=True)
