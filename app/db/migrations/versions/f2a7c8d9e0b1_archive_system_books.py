"""Archive system books before physical storage cleanup.

Revision ID: f2a7c8d9e0b1
Revises: e8f4c2b1a9d0
Create Date: 2026-08-10
"""

from alembic import op
import sqlalchemy as sa


revision = "f2a7c8d9e0b1"
down_revision = "e8f4c2b1a9d0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("books", sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_books_archived_at", "books", ["archived_at"])


def downgrade() -> None:
    op.drop_index("ix_books_archived_at", table_name="books")
    op.drop_column("books", "archived_at")
