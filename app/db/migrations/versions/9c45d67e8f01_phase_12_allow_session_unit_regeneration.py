"""phase 12 allow session unit regeneration

Revision ID: 9c45d67e8f01
Revises: 8b34c56d7e90
Create Date: 2026-06-11
"""

from typing import Sequence, Union

from alembic import op

revision: str = "9c45d67e8f01"
down_revision: Union[str, None] = "8b34c56d7e90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_reading_plan_session_units_plan_unit", "reading_plan_session_units", type_="unique")
    op.create_index("ix_reading_plan_session_units_plan_unit", "reading_plan_session_units", ["plan_id", "learning_unit_id"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_session_units_plan_unit", table_name="reading_plan_session_units")
    op.create_unique_constraint(
        "uq_reading_plan_session_units_plan_unit",
        "reading_plan_session_units",
        ["plan_id", "learning_unit_id"],
    )
