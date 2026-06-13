"""phase 12 allow session regeneration history

Revision ID: 8b34c56d7e90
Revises: 7a12b34c56d8
Create Date: 2026-06-11
"""

from typing import Sequence, Union

from alembic import op

revision: str = "8b34c56d7e90"
down_revision: Union[str, None] = "7a12b34c56d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_reading_plan_sessions_plan_index", "reading_plan_sessions", type_="unique")
    op.create_index("ix_reading_plan_sessions_plan_index", "reading_plan_sessions", ["plan_id", "session_index"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_sessions_plan_index", table_name="reading_plan_sessions")
    op.create_unique_constraint(
        "uq_reading_plan_sessions_plan_index",
        "reading_plan_sessions",
        ["plan_id", "session_index"],
    )
