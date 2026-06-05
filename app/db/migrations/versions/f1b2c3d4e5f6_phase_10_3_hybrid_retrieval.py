"""phase 10.3 hybrid retrieval

Revision ID: f1b2c3d4e5f6
Revises: f0a1b2c3d4e5
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f0a1b2c3d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create extension if not exists pg_trgm")
    op.add_column(
        "book_section_knowledge",
        sa.Column("search_text", sa.Text(), server_default="", nullable=False),
    )
    op.execute(
        """
        create index if not exists ix_bsk_search_text_trgm
        on book_section_knowledge
        using gin (search_text gin_trgm_ops)
        """
    )
    op.execute(
        """
        create index if not exists ix_bsk_content_fts_simple
        on book_section_knowledge
        using gin (to_tsvector('simple', content))
        """
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
            and (
              filter_section_ids is null
              or cardinality(filter_section_ids) = 0
              or bsk.section_id = any(filter_section_ids)
            )
            and 1 - (bsk.embedding <=> query_embedding) > match_threshold
          order by bsk.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )
    op.execute(
        """
        drop function if exists match_book_section_knowledge_lexical(
          text,
          text,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge_lexical(
          query_text text,
          normalized_query_text text,
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
          lexical_score float
        )
        language sql stable
        as $$
          with fts_candidates as (
            select
              bsk.id,
              bsk.book_id,
              bsk.section_id,
              bs.path as section_path,
              bs.title as section_title,
              bsk.chunk_index,
              bsk.content,
              ts_rank_cd(
                to_tsvector('simple', bsk.content),
                websearch_to_tsquery('simple', query_text)
              )::float as score
            from book_section_knowledge bsk
            join book_sections bs on bs.id = bsk.section_id
            where bsk.book_id = any(filter_book_ids)
              and (
                filter_section_ids is null
                or cardinality(filter_section_ids) = 0
                or bsk.section_id = any(filter_section_ids)
              )
              and coalesce(query_text, '') <> ''
              and to_tsvector('simple', bsk.content) @@ websearch_to_tsquery('simple', query_text)
            order by score desc
            limit match_count
          ),
          trigram_candidates as (
            select
              bsk.id,
              bsk.book_id,
              bsk.section_id,
              bs.path as section_path,
              bs.title as section_title,
              bsk.chunk_index,
              bsk.content,
              word_similarity(normalized_query_text, bsk.search_text)::float as score
            from book_section_knowledge bsk
            join book_sections bs on bs.id = bsk.section_id
            where bsk.book_id = any(filter_book_ids)
              and (
                filter_section_ids is null
                or cardinality(filter_section_ids) = 0
                or bsk.section_id = any(filter_section_ids)
              )
              and coalesce(normalized_query_text, '') <> ''
              and normalized_query_text <% bsk.search_text
            order by score desc
            limit match_count
          )
          select
            merged.id,
            merged.book_id,
            merged.section_id,
            merged.section_path,
            merged.section_title,
            merged.chunk_index,
            merged.content,
            max(merged.score) as lexical_score
          from (
            select * from fts_candidates
            union all
            select * from trigram_candidates
          ) merged
          group by
            merged.id,
            merged.book_id,
            merged.section_id,
            merged.section_path,
            merged.section_title,
            merged.chunk_index,
            merged.content
          order by max(merged.score) desc
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop function if exists match_book_section_knowledge_lexical(
          text,
          text,
          integer,
          uuid[],
          uuid[]
        );
        """
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
    op.execute("drop index if exists ix_bsk_content_fts_simple")
    op.execute("drop index if exists ix_bsk_search_text_trgm")
    op.drop_column("book_section_knowledge", "search_text")
