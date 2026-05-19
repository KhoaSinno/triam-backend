"""add document type and unique constraints

Revision ID: b8e4f2a7c9d1
Revises: 91b0326bdf19
Create Date: 2026-05-19 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8e4f2a7c9d1"
down_revision: Union[str, Sequence[str], None] = "91b0326bdf19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("books", sa.Column("document_type", sa.Text(), nullable=True))

    op.execute(
        """
        UPDATE books
        SET document_type = CASE
            WHEN lower(file_url) LIKE '%.pdf%' THEN 'pdf'
            WHEN lower(file_url) LIKE '%.epub%' THEN 'epub'
            WHEN lower(file_url) LIKE '%.docx%' THEN 'docx'
            ELSE document_type
        END
        WHERE document_type IS NULL
        """
    )

    op.create_unique_constraint(
        "uq_chapters_book_id_chapter_index",
        "chapters",
        ["book_id", "chapter_index"],
    )
    op.create_unique_constraint(
        "uq_segments_chapter_mode_segment_index",
        "chapter_segments",
        ["chapter_id", "mode", "segment_index"],
    )
    op.create_unique_constraint(
        "uq_book_knowledge_chapter_chunk_index",
        "book_knowledge",
        ["chapter_id", "chunk_index"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_book_knowledge_chapter_chunk_index", "book_knowledge", type_="unique")
    op.drop_constraint("uq_segments_chapter_mode_segment_index", "chapter_segments", type_="unique")
    op.drop_constraint("uq_chapters_book_id_chapter_index", "chapters", type_="unique")
    op.drop_column("books", "document_type")
