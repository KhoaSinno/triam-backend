"""phase 14.1 clean reading plan schedule config

Revision ID: c15d3e4f5061
Revises: b14c2d3e4f50
Create Date: 2026-06-13
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c15d3e4f5061"
down_revision: Union[str, None] = "b14c2d3e4f50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DAY_TO_WEEKDAY_CASE = """
case lower(trim(day.value))
  when 'mon' then 0
  when 'monday' then 0
  when 'tue' then 1
  when 'tuesday' then 1
  when 'wed' then 2
  when 'wednesday' then 2
  when 'thu' then 3
  when 'thursday' then 3
  when 'fri' then 4
  when 'friday' then 4
  when 'sat' then 5
  when 'saturday' then 5
  when 'sun' then 6
  when 'sunday' then 6
  else null
end
"""


WEEKDAY_TO_DAY_CASE = """
case s.weekday
  when 0 then 'Mon'
  when 1 then 'Tue'
  when 2 then 'Wed'
  when 3 then 'Thu'
  when 4 then 'Fri'
  when 5 then 'Sat'
  when 6 then 'Sun'
  else s.weekday::text
end
"""


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")
    op.execute(
        f"""
        insert into reading_plan_schedule_slots (
            id,
            user_id,
            plan_id,
            book_id,
            weekday,
            reminder_time,
            timezone,
            is_active,
            created_at,
            updated_at
        )
        select
            gen_random_uuid(),
            b.user_id,
            rp.id,
            rp.book_id,
            {DAY_TO_WEEKDAY_CASE} as weekday,
            coalesce(rp.reminder_time, '20:00') as reminder_time,
            coalesce(ns.timezone, 'Asia/Ho_Chi_Minh') as timezone,
            (
                rp.status = 'active'
                and not exists (
                    select 1
                    from reading_plan_schedule_slots active_conflict
                    where active_conflict.user_id = b.user_id
                      and active_conflict.weekday = {DAY_TO_WEEKDAY_CASE}
                      and active_conflict.reminder_time = coalesce(rp.reminder_time, '20:00')
                      and active_conflict.is_active is true
                )
            ) as is_active,
            now(),
            now()
        from reading_plans rp
        join books b on b.id = rp.book_id
        left join notification_settings ns on ns.user_id = b.user_id
        cross join lateral jsonb_array_elements_text(rp.schedule_config) as day(value)
        where rp.schedule_config is not null
          and jsonb_typeof(rp.schedule_config) = 'array'
          and {DAY_TO_WEEKDAY_CASE} is not null
          and not exists (
              select 1
              from reading_plan_schedule_slots existing
              where existing.plan_id = rp.id
          )
        """
    )
    op.drop_column("reading_plans", "schedule_config")


def downgrade() -> None:
    op.add_column(
        "reading_plans",
        sa.Column("schedule_config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute(
        f"""
        update reading_plans rp
        set schedule_config = coalesce(
            (
                select jsonb_agg({WEEKDAY_TO_DAY_CASE} order by s.weekday)
                from reading_plan_schedule_slots s
                where s.plan_id = rp.id
            ),
            '[]'::jsonb
        )
        """
    )
