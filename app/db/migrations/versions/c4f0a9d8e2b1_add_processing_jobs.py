"""add processing jobs

Revision ID: c4f0a9d8e2b1
Revises: b8e4f2a7c9d1
Create Date: 2026-05-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c4f0a9d8e2b1"
down_revision: Union[str, None] = "b8e4f2a7c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


processing_job_type = postgresql.ENUM(
    "UPLOAD",
    "GENERATE_PLAN",
    "SWITCH_MODE",
    "NOTIFICATION",
    "REVIEW",
    name="processingjobtype",
    create_type=False,
)
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
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE processingjobtype AS ENUM ('UPLOAD', 'GENERATE_PLAN', 'SWITCH_MODE', 'NOTIFICATION', 'REVIEW');
        EXCEPTION WHEN duplicate_object THEN null;
        END $$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE processingjobstatus AS ENUM ('QUEUED', 'PROCESSING', 'PARTIAL_READY', 'READY', 'ERROR', 'CANCELLED');
        EXCEPTION WHEN duplicate_object THEN null;
        END $$;
        """
    )

    op.create_table(
        "processing_jobs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=True),
        sa.Column("job_type", processing_job_type, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("mode", plan_mode, nullable=True),
        sa.Column("progress_percent", sa.Integer(), server_default="0", nullable=False),
        sa.Column("current_step", sa.Text(), nullable=True),
        sa.Column("total_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("done_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("failed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_processing_jobs_book_id", "processing_jobs", ["book_id"])
    op.create_index("ix_processing_jobs_job_type", "processing_jobs", ["job_type"])
    op.create_index("ix_processing_jobs_status", "processing_jobs", ["status"])
    op.create_index("ix_processing_jobs_user_id", "processing_jobs", ["user_id"])
    op.create_check_constraint(
        "ck_books_status_known",
        "books",
        "status IN ('draft', 'processing', 'partial_ready', 'ready', 'error') OR status IS NULL",
    )


def downgrade() -> None:
    op.drop_constraint("ck_books_status_known", "books", type_="check")
    op.drop_index("ix_processing_jobs_user_id", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_status", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_job_type", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_book_id", table_name="processing_jobs")
    op.drop_table("processing_jobs")
    processing_job_status.drop(op.get_bind(), checkfirst=True)
    processing_job_type.drop(op.get_bind(), checkfirst=True)
