"""phase_26_add_ai_summary_columns_to_books

Revision ID: 1c8e597332f3
Revises: b14a05b2dfeb
Create Date: 2026-07-21 09:11:48.100871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c8e597332f3'
down_revision: Union[str, Sequence[str], None] = 'b14a05b2dfeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('books', sa.Column('ai_summary', sa.JSON(), nullable=True))
    op.add_column('books', sa.Column('ai_summary_status', sa.Text(), server_default='pending', nullable=False))
    op.add_column('books', sa.Column('ai_summary_error', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('books', 'ai_summary_error')
    op.drop_column('books', 'ai_summary_status')
    op.drop_column('books', 'ai_summary')
