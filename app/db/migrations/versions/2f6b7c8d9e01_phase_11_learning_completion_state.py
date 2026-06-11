"""phase 11 learning completion state

Revision ID: 2f6b7c8d9e01
Revises: f1b2c3d4e5f6
Create Date: 2026-06-11
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "2f6b7c8d9e01"
down_revision: Union[str, None] = "f1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")

    op.add_column("reading_plans", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("reading_plans", sa.Column("paused_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("reading_plans", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_reading_plans_completed_at", "reading_plans", ["completed_at"])

    op.create_table(
        "book_learning_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", sa.Text(), server_default="not_started", nullable=False),
        sa.Column("book_progress_percent", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("playable_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_learning_unit_id", sa.UUID(), nullable=True),
        sa.Column("last_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=True),
        sa.Column("position_ms", sa.Integer(), server_default="0", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["last_learning_unit_id"], ["learning_units.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["last_segment_id"], ["learning_unit_segments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "book_id", "mode", name="uq_book_learning_state_user_book_mode"),
    )
    op.create_index("ix_book_learning_states_user_id", "book_learning_states", ["user_id"])
    op.create_index("ix_book_learning_states_book_id", "book_learning_states", ["book_id"])
    op.create_index("ix_book_learning_states_mode", "book_learning_states", ["mode"])
    op.create_index("ix_book_learning_states_status", "book_learning_states", ["status"])
    op.create_index("ix_book_learning_states_last_activity_at", "book_learning_states", ["last_activity_at"])
    op.create_index("ix_book_learning_states_completed_at", "book_learning_states", ["completed_at"])
    op.create_index("ix_book_learning_states_user_status", "book_learning_states", ["user_id", "status"])
    op.create_index("ix_book_learning_states_book_mode", "book_learning_states", ["book_id", "mode"])

    op.execute(
        """
        with playable_units as (
            select
                lu.user_id,
                lu.book_id,
                lu.mode,
                lu.id as learning_unit_id
            from learning_units lu
            where exists (
                select 1
                from learning_unit_segments seg
                where seg.learning_unit_id = lu.id
            )
        ),
        latest_progress as (
            select distinct on (lup.user_id, lup.book_id, lup.mode)
                lup.user_id,
                lup.book_id,
                lup.mode,
                lup.learning_unit_id,
                lup.current_segment_id,
                lup.last_segment_index,
                lup.position_ms,
                coalesce(lup.last_activity_at, lup.updated_at) as latest_at
            from learning_unit_progress lup
            order by
                lup.user_id,
                lup.book_id,
                lup.mode,
                coalesce(lup.last_activity_at, lup.updated_at) desc nulls last,
                lup.updated_at desc
        ),
        summary as (
            select
                pu.user_id,
                pu.book_id,
                pu.mode,
                count(*)::int as playable_units,
                count(lup.id) filter (where lup.status = 'COMPLETED')::int as completed_units,
                coalesce(round(avg(coalesce(lup.max_progress_percent, 0)))::int, 0) as book_progress_percent,
                min(lup.started_at) as started_at,
                max(coalesce(lup.last_activity_at, lup.updated_at)) as last_activity_at,
                max(lup.completed_at) as latest_completed_at
            from playable_units pu
            left join learning_unit_progress lup
                on lup.user_id = pu.user_id
                and lup.book_id = pu.book_id
                and lup.mode = pu.mode
                and lup.learning_unit_id = pu.learning_unit_id
            group by pu.user_id, pu.book_id, pu.mode
        )
        insert into book_learning_states (
            id,
            user_id,
            book_id,
            mode,
            status,
            book_progress_percent,
            completed_units,
            playable_units,
            last_learning_unit_id,
            last_segment_id,
            last_segment_index,
            position_ms,
            started_at,
            last_activity_at,
            completed_at
        )
        select
            gen_random_uuid(),
            s.user_id,
            s.book_id,
            s.mode,
            case
                when s.playable_units > 0 and s.completed_units >= s.playable_units then 'completed'
                when s.last_activity_at is not null then 'in_progress'
                else 'not_started'
            end as status,
            s.book_progress_percent,
            s.completed_units,
            s.playable_units,
            lp.learning_unit_id,
            lp.current_segment_id,
            lp.last_segment_index,
            coalesce(lp.position_ms, 0),
            s.started_at,
            s.last_activity_at,
            case
                when s.playable_units > 0 and s.completed_units >= s.playable_units then s.latest_completed_at
                else null
            end as completed_at
        from summary s
        left join latest_progress lp
            on lp.user_id = s.user_id
            and lp.book_id = s.book_id
            and lp.mode = s.mode
        on conflict (user_id, book_id, mode) do nothing;
        """
    )

    op.execute(
        """
        update reading_plans rp
        set
            status = 'completed',
            completed_at = bls.completed_at,
            updated_at = now()
        from book_learning_states bls
        where rp.book_id = bls.book_id
            and rp.mode = bls.mode
            and bls.status = 'completed';
        """
    )

    op.execute(
        """
        delete from reading_plan_schedule_slots slots
        using reading_plans rp
        where slots.plan_id = rp.id
            and rp.status = 'completed';
        """
    )


def downgrade() -> None:
    op.drop_index("ix_book_learning_states_book_mode", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_user_status", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_completed_at", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_last_activity_at", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_status", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_mode", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_book_id", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_user_id", table_name="book_learning_states")
    op.drop_table("book_learning_states")

    op.drop_index("ix_reading_plans_completed_at", table_name="reading_plans")
    op.drop_column("reading_plans", "completed_at")
    op.drop_column("reading_plans", "paused_at")
    op.drop_column("reading_plans", "started_at")
