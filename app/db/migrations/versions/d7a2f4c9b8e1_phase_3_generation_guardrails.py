"""phase 3 generation guardrails

Revision ID: d7a2f4c9b8e1
Revises: c4f0a9d8e2b1
Create Date: 2026-05-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d7a2f4c9b8e1"
down_revision: Union[str, None] = "c4f0a9d8e2b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)
processing_job_status = postgresql.ENUM(
    "QUEUED",
    "PROCESSING",
    "PARTIAL_READY",
    "READY",
    "ERROR",
    "CANCELLED",
    name="processingjobstatus",
    create_type=False,
)


def upgrade() -> None:
    op.add_column("processing_jobs", sa.Column("estimated_input_tokens", sa.Integer(), nullable=True))
    op.add_column("processing_jobs", sa.Column("estimated_audio_seconds", sa.Integer(), nullable=True))

    op.create_table(
        "chapter_processing_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("raw_text_char_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("estimated_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("estimated_audio_seconds", sa.Integer(), server_default="0", nullable=False),
        sa.Column("main_segment_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["processing_jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chapter_id", "mode", name="uq_chapter_processing_state_chapter_mode"),
    )
    op.create_index("ix_chapter_processing_states_book_id", "chapter_processing_states", ["book_id"])
    op.create_index("ix_chapter_processing_states_chapter_id", "chapter_processing_states", ["chapter_id"])
    op.create_index("ix_chapter_processing_states_job_id", "chapter_processing_states", ["job_id"])
    op.create_index("ix_chapter_processing_states_status", "chapter_processing_states", ["status"])
    op.create_index("ix_chapter_processing_states_user_id", "chapter_processing_states", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_chapter_processing_states_user_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_status", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_job_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_chapter_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_book_id", table_name="chapter_processing_states")
    op.drop_table("chapter_processing_states")
    op.drop_column("processing_jobs", "estimated_audio_seconds")
    op.drop_column("processing_jobs", "estimated_input_tokens")
