"""phase 13 calendar session actions

Revision ID: a13f1e2d3c4b
Revises: 9c45d67e8f01
Create Date: 2026-06-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a13f1e2d3c4b"
down_revision: Union[str, None] = "9c45d67e8f01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("reading_plan_sessions", sa.Column("missed_notified_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("reading_plan_sessions", "missed_notified_at")
