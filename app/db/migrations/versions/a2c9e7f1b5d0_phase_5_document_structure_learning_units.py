"""phase 5 document structure learning units

Revision ID: a2c9e7f1b5d0
Revises: f6a8c2d4e9b1
Create Date: 2026-05-28
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a2c9e7f1b5d0"
down_revision: Union[str, None] = "f6a8c2d4e9b1"
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
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.add_column("books", sa.Column("total_sections", sa.Integer(), nullable=True))
    op.add_column("books", sa.Column("total_units", sa.Integer(), nullable=True))

    op.create_table(
        "book_sections",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column("section_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("page_start", sa.Integer(), nullable=True),
        sa.Column("page_end", sa.Integer(), nullable=True),
        sa.Column("source_href", sa.Text(), nullable=True),
        sa.Column("source_anchor", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "path", name="uq_book_sections_book_path"),
        sa.UniqueConstraint("book_id", "section_index", name="uq_book_sections_book_index"),
    )
    op.create_index("ix_book_sections_book_id", "book_sections", ["book_id"])
    op.create_index("ix_book_sections_parent_id", "book_sections", ["parent_id"])

    op.create_table(
        "learning_units",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("unit_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("unit_type", sa.Text(), nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("source_text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_audio_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("main_segment_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("review_audio_url", sa.Text(), nullable=True),
        sa.Column("review_text", sa.Text(), nullable=True),
        sa.Column("planner_reason", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "mode", "unit_index", name="uq_learning_units_book_mode_index"),
    )
    op.create_index("ix_learning_units_book_id", "learning_units", ["book_id"])
    op.create_index("ix_learning_units_mode", "learning_units", ["mode"])
    op.create_index("ix_learning_units_status", "learning_units", ["status"])
    op.create_index("ix_learning_units_user_id", "learning_units", ["user_id"])

    op.create_table(
        "learning_unit_sources",
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("section_id", sa.UUID(), nullable=False),
        sa.Column("source_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("learning_unit_id", "section_id"),
    )

    op.create_table(
        "learning_unit_segments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("learning_unit_id", "segment_index", name="uq_learning_unit_segments_unit_index"),
    )
    op.create_index("ix_learning_unit_segments_learning_unit_id", "learning_unit_segments", ["learning_unit_id"])

    op.create_table(
        "learning_unit_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["current_segment_id"], ["learning_unit_segments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "learning_unit_id", name="uq_unit_progress_user_unit"),
    )
    op.create_index("ix_learning_unit_progress_book_id", "learning_unit_progress", ["book_id"])
    op.create_index("ix_learning_unit_progress_completed_at", "learning_unit_progress", ["completed_at"])
    op.create_index("ix_learning_unit_progress_last_activity_at", "learning_unit_progress", ["last_activity_at"])
    op.create_index("ix_learning_unit_progress_learning_unit_id", "learning_unit_progress", ["learning_unit_id"])
    op.create_index("ix_learning_unit_progress_status", "learning_unit_progress", ["status"])
    op.create_index("ix_learning_unit_progress_user_id", "learning_unit_progress", ["user_id"])

    op.add_column("book_knowledge", sa.Column("learning_unit_id", sa.UUID(), nullable=True))
    op.alter_column("book_knowledge", "chapter_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key("fk_book_knowledge_learning_unit_id", "book_knowledge", "learning_units", ["learning_unit_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_book_knowledge_learning_unit_id", "book_knowledge", ["learning_unit_id"])
    op.create_unique_constraint("uq_book_knowledge_unit_chunk_index", "book_knowledge", ["learning_unit_id", "chunk_index"])

    op.add_column("spaced_review_items", sa.Column("learning_unit_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_unit_progress_id", sa.UUID(), nullable=True))
    op.alter_column("spaced_review_items", "chapter_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key("fk_spaced_review_items_learning_unit_id", "spaced_review_items", "learning_units", ["learning_unit_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_spaced_review_items_source_unit_progress_id", "spaced_review_items", "learning_unit_progress", ["source_unit_progress_id"], ["id"], ondelete="SET NULL")
    op.create_index("ix_spaced_review_items_learning_unit_id", "spaced_review_items", ["learning_unit_id"])
    op.create_index("ix_spaced_review_items_source_unit_progress_id", "spaced_review_items", ["source_unit_progress_id"])

    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
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


def downgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.drop_index("ix_spaced_review_items_source_unit_progress_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_learning_unit_id", table_name="spaced_review_items")
    op.drop_constraint("fk_spaced_review_items_source_unit_progress_id", "spaced_review_items", type_="foreignkey")
    op.drop_constraint("fk_spaced_review_items_learning_unit_id", "spaced_review_items", type_="foreignkey")
    op.alter_column("spaced_review_items", "chapter_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("spaced_review_items", "source_unit_progress_id")
    op.drop_column("spaced_review_items", "learning_unit_id")
    op.drop_constraint("uq_book_knowledge_unit_chunk_index", "book_knowledge", type_="unique")
    op.drop_index("ix_book_knowledge_learning_unit_id", table_name="book_knowledge")
    op.drop_constraint("fk_book_knowledge_learning_unit_id", "book_knowledge", type_="foreignkey")
    op.alter_column("book_knowledge", "chapter_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("book_knowledge", "learning_unit_id")
    op.drop_index("ix_learning_unit_progress_user_id", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_status", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_learning_unit_id", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_last_activity_at", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_completed_at", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_book_id", table_name="learning_unit_progress")
    op.drop_table("learning_unit_progress")
    op.drop_index("ix_learning_unit_segments_learning_unit_id", table_name="learning_unit_segments")
    op.drop_table("learning_unit_segments")
    op.drop_table("learning_unit_sources")
    op.drop_index("ix_learning_units_user_id", table_name="learning_units")
    op.drop_index("ix_learning_units_status", table_name="learning_units")
    op.drop_index("ix_learning_units_mode", table_name="learning_units")
    op.drop_index("ix_learning_units_book_id", table_name="learning_units")
    op.drop_table("learning_units")
    op.drop_index("ix_book_sections_parent_id", table_name="book_sections")
    op.drop_index("ix_book_sections_book_id", table_name="book_sections")
    op.drop_table("book_sections")
    op.drop_column("books", "total_units")
    op.drop_column("books", "total_sections")

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
