from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

WEEKDAY_ALIASES = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def parse_hhmm(value: str) -> time:
    parts = value.split(":", 1)
    if len(parts) != 2:
        raise ValueError("Time must use HH:MM format.")
    hour, minute = int(parts[0]), int(parts[1])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("Time must use HH:MM 24-hour format.")
    return time(hour=hour, minute=minute)


def to_local(now_utc: datetime, timezone_name: str) -> datetime:
    return ensure_aware_utc(now_utc).astimezone(ZoneInfo(timezone_name))


def is_quiet_time(local_dt: datetime, quiet_start: str, quiet_end: str) -> bool:
    start = parse_hhmm(quiet_start)
    end = parse_hhmm(quiet_end)
    current = local_dt.time()
    if start <= end:
        return start <= current < end
    return current >= start or current < end


def shift_out_of_quiet_hours(due_at_utc: datetime, timezone_name: str, quiet_start: str, quiet_end: str) -> datetime:
    local_due = to_local(due_at_utc, timezone_name)
    if not is_quiet_time(local_due, quiet_start, quiet_end):
        return ensure_aware_utc(due_at_utc)

    end_time = parse_hhmm(quiet_end)
    start_time = parse_hhmm(quiet_start)
    if start_time <= end_time:
        shifted_local = local_due.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)
    elif local_due.time() < end_time:
        shifted_local = local_due.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)
    else:
        next_day = local_due.date() + timedelta(days=1)
        shifted_local = datetime.combine(next_day, end_time, tzinfo=local_due.tzinfo)
    return shifted_local.astimezone(timezone.utc)


def local_day_bounds_utc(local_day: date, timezone_name: str) -> tuple[datetime, datetime]:
    tz = ZoneInfo(timezone_name)
    start_local = datetime.combine(local_day, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def reminder_due_at_for_today(
    *,
    now_utc: datetime,
    timezone_name: str,
    reminder_time: str,
) -> datetime:
    local_now = to_local(now_utc, timezone_name)
    reminder_local_time = parse_hhmm(reminder_time)
    reminder_local = datetime.combine(local_now.date(), reminder_local_time, tzinfo=local_now.tzinfo)
    return reminder_local.astimezone(timezone.utc)
