"""phase 14 drop legacy book knowledge

Revision ID: b14c2d3e4f50
Revises: a13f1e2d3c4b
Create Date: 2026-06-13
"""

from typing import Sequence, Union

from alembic import op

revision: str = "b14c2d3e4f50"
down_revision: Union[str, None] = "a13f1e2d3c4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.execute("drop table if exists book_knowledge cascade")


def downgrade() -> None:
    # `book_knowledge` stored legacy learning-unit embeddings. The table data
    # cannot be reconstructed by Alembic after a destructive cleanup; restore a
    # database backup if this migration must be rolled back in production.
    pass
