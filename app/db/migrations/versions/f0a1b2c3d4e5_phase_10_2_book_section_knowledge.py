"""phase 10.2 book section knowledge

Revision ID: f0a1b2c3d4e5
Revises: 2b7c9d1e4f6a
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "f0a1b2c3d4e5"
down_revision: Union[str, Sequence[str], None] = "2b7c9d1e4f6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book_section_knowledge",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("section_id", sa.UUID(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("embedding_model", sa.Text(), nullable=False),
        sa.Column("embedding_version", sa.Text(), nullable=False),
        sa.Column("char_count", sa.Integer(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("section_id", "chunk_index", "embedding_version", name="uq_book_section_knowledge_section_chunk_version"),
        sa.UniqueConstraint("section_id", "content_hash", "embedding_version", name="uq_book_section_knowledge_section_hash_version"),
    )
    op.create_index(op.f("ix_book_section_knowledge_book_id"), "book_section_knowledge", ["book_id"])
    op.create_index(op.f("ix_book_section_knowledge_section_id"), "book_section_knowledge", ["section_id"])
    op.create_index("ix_bsk_book_version", "book_section_knowledge", ["book_id", "embedding_version"])
    op.create_index("ix_bsk_section_version", "book_section_knowledge", ["section_id", "embedding_version"])
    op.create_index("ix_bsk_book_section_version", "book_section_knowledge", ["book_id", "section_id", "embedding_version"])
    op.create_index(
        "ix_bsk_embedding_hnsw",
        "book_section_knowledge",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )

    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[],
          filter_section_ids uuid[] default null
        )
        returns table (
          id integer,
          book_id uuid,
          section_id uuid,
          section_path text,
          section_title text,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            bsk.id,
            bsk.book_id,
            bsk.section_id,
            bs.path as section_path,
            bs.title as section_title,
            bsk.chunk_index,
            bsk.content,
            1 - (bsk.embedding <=> query_embedding) as similarity
          from book_section_knowledge bsk
          join book_sections bs on bs.id = bsk.section_id
          where bsk.embedding is not null
            and bsk.book_id = any(filter_book_ids)
            and (filter_section_ids is null or bsk.section_id = any(filter_section_ids))
            and 1 - (bsk.embedding <=> query_embedding) > match_threshold
          order by bsk.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.drop_table("book_section_knowledge")
