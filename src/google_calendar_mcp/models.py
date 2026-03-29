from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo


def compact_event(event: dict[str, Any]) -> dict[str, Any]:
    start = event.get("start") or {}
    end = event.get("end") or {}
    return {
        "id": event.get("id"),
        "title": event.get("summary"),
        "start": start.get("dateTime") or start.get("date"),
        "end": end.get("dateTime") or end.get("date"),
        "location": event.get("location"),
        "status": event.get("status"),
        "html_link": event.get("htmlLink"),
    }


def event_time_fields(start: str, end: str, timezone: str | None) -> tuple[dict[str, str], dict[str, str]]:
    is_date = len(start) == 10 and len(end) == 10
    if is_date:
        return {"date": start}, {"date": end}

    if bool(len(start) == 10) != bool(len(end) == 10):
        raise ValueError("start and end must both be dates or both be datetimes")

    tz = timezone or "UTC"
    return {"dateTime": start, "timeZone": tz}, {"dateTime": end, "timeZone": tz}


def normalize_time_min(value: str, timezone: str) -> str:
    if len(value) == 10:
        zone = ZoneInfo(timezone)
        return datetime.fromisoformat(value).replace(tzinfo=zone).isoformat()
    return value


def normalize_time_max(value: str, timezone: str) -> str:
    if len(value) == 10:
        zone = ZoneInfo(timezone)
        date = datetime.fromisoformat(value) + timedelta(days=1)
        return date.replace(tzinfo=zone).isoformat()
    return value
