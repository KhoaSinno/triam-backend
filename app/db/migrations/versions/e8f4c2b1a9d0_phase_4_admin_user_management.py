"""phase 4 admin user management

Revision ID: e8f4c2b1a9d0
Revises: 1c8e597332f3
Create Date: 2026-08-09
"""

from typing import Sequence, Union

from alembic import op


revision: str = "e8f4c2b1a9d0"
down_revision: Union[str, Sequence[str], None] = "1c8e597332f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'ADMIN_ANNOUNCEMENT'")
    op.create_index(
        "ix_learning_unit_progress_user_status",
        "learning_unit_progress",
        ["user_id", "status"],
    )
    op.create_index(
        "ix_spaced_review_items_user_status",
        "spaced_review_items",
        ["user_id", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_spaced_review_items_user_status", table_name="spaced_review_items")
    op.drop_index("ix_learning_unit_progress_user_status", table_name="learning_unit_progress")
    # PostgreSQL does not support removing an enum value safely. The enum value
    # remains unused when this revision is downgraded.
