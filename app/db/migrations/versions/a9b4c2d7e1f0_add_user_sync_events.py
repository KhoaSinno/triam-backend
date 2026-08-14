"""add durable user sync events

Revision ID: a9b4c2d7e1f0
Revises: f2a7c8d9e0b1
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "a9b4c2d7e1f0"
down_revision = "f2a7c8d9e0b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_sync_events",
        sa.Column("event_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain", sa.Text(), nullable=False),
        sa.Column("entity_id", sa.Text(), nullable=False),
        sa.Column("operation", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_user_sync_events_user_event", "user_sync_events", ["user_id", "event_id"])


def downgrade() -> None:
    op.drop_index("ix_user_sync_events_user_event", table_name="user_sync_events")
    op.drop_table("user_sync_events")
