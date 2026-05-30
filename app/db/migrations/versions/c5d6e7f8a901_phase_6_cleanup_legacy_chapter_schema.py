"""phase 6 cleanup legacy chapter schema

Revision ID: c5d6e7f8a901
Revises: a2c9e7f1b5d0
Create Date: 2026-05-29
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c5d6e7f8a901"
down_revision: Union[str, None] = "a2c9e7f1b5d0"
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
learning_progress_status = postgresql.ENUM(
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    name="learningprogressstatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")

    op.execute("alter table if exists book_knowledge drop column if exists chapter_id cascade")
    op.execute("alter table if exists spaced_review_items drop column if exists source_progress_id cascade")
    op.execute("alter table if exists spaced_review_items drop column if exists chapter_id cascade")
    op.execute("alter table if exists books drop column if exists total_chapters")

    op.execute("drop table if exists chapter_learning_progress cascade")
    op.execute("drop table if exists chapter_processing_states cascade")
    op.execute("drop table if exists chapter_segments cascade")
    op.execute("drop table if exists chapters cascade")

    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          learning_unit_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.learning_unit_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and book_knowledge.learning_unit_id is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")

    op.add_column("books", sa.Column("total_chapters", sa.Integer(), nullable=True))

    op.create_table(
        "chapters",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("review_audio_url", sa.Text(), nullable=True),
        sa.Column("review_text", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "chapter_index", name="uq_chapters_book_id_chapter_index"),
    )
    op.create_index("ix_chapters_book_id", "chapters", ["book_id"])

    op.create_table(
        "chapter_segments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chapter_id", "mode", "segment_index", name="uq_segments_chapter_mode_segment_index"),
    )
    op.create_index("ix_chapter_segments_chapter_id", "chapter_segments", ["chapter_id"])

    op.create_table(
        "chapter_processing_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("raw_text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_audio_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("main_segment_count", sa.Integer(), nullable=False, server_default="0"),
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
    op.create_index("ix_chapter_processing_states_user_id", "chapter_processing_states", ["user_id"])
    op.create_index("ix_chapter_processing_states_book_id", "chapter_processing_states", ["book_id"])
    op.create_index("ix_chapter_processing_states_chapter_id", "chapter_processing_states", ["chapter_id"])
    op.create_index("ix_chapter_processing_states_job_id", "chapter_processing_states", ["job_id"])
    op.create_index("ix_chapter_processing_states_status", "chapter_processing_states", ["status"])

    op.create_table(
        "chapter_learning_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("current_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("position_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("listened_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_progress_percent", sa.Integer(), nullable=False, server_default="0"),
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

    op.add_column("book_knowledge", sa.Column("chapter_id", sa.UUID(), nullable=True))
    op.create_index("ix_book_knowledge_chapter_id", "book_knowledge", ["chapter_id"])
    op.create_foreign_key("book_knowledge_chapter_id_fkey", "book_knowledge", "chapters", ["chapter_id"], ["id"], ondelete="CASCADE")
    op.create_unique_constraint("uq_book_knowledge_chapter_chunk_index", "book_knowledge", ["chapter_id", "chunk_index"])

    op.add_column("spaced_review_items", sa.Column("chapter_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_progress_id", sa.UUID(), nullable=True))
    op.create_index("ix_spaced_review_items_chapter_id", "spaced_review_items", ["chapter_id"])
    op.create_index("ix_spaced_review_items_source_progress_id", "spaced_review_items", ["source_progress_id"])
    op.create_foreign_key("spaced_review_items_chapter_id_fkey", "spaced_review_items", "chapters", ["chapter_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(
        "spaced_review_items_source_progress_id_fkey",
        "spaced_review_items",
        "chapter_learning_progress",
        ["source_progress_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          learning_unit_id uuid,
          chapter_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.learning_unit_id,
            book_knowledge.chapter_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )
