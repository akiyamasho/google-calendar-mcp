from google_calendar_mcp.models import (
    compact_event,
    event_time_fields,
    normalize_time_max,
    normalize_time_min,
)


def test_compact_event_for_datetime_event() -> None:
    event = {
        "id": "abc",
        "summary": "Lunch",
        "start": {"dateTime": "2026-04-01T12:00:00+09:00"},
        "end": {"dateTime": "2026-04-01T13:00:00+09:00"},
        "location": "Tokyo",
        "status": "confirmed",
        "htmlLink": "https://example.com",
    }

    assert compact_event(event) == {
        "id": "abc",
        "title": "Lunch",
        "start": "2026-04-01T12:00:00+09:00",
        "end": "2026-04-01T13:00:00+09:00",
        "location": "Tokyo",
        "status": "confirmed",
        "html_link": "https://example.com",
    }


def test_event_time_fields_for_all_day_event() -> None:
    start, end = event_time_fields("2026-04-01", "2026-04-02", "Asia/Tokyo")
    assert start == {"date": "2026-04-01"}
    assert end == {"date": "2026-04-02"}


def test_event_time_fields_for_timed_event() -> None:
    start, end = event_time_fields(
        "2026-04-01T12:00:00+09:00",
        "2026-04-01T13:00:00+09:00",
        "Asia/Tokyo",
    )
    assert start == {"dateTime": "2026-04-01T12:00:00+09:00", "timeZone": "Asia/Tokyo"}
    assert end == {"dateTime": "2026-04-01T13:00:00+09:00", "timeZone": "Asia/Tokyo"}


def test_normalize_time_range_for_dates() -> None:
    assert normalize_time_min("2026-04-01", "Asia/Tokyo").startswith("2026-04-01T00:00:00")
    assert normalize_time_max("2026-04-01", "Asia/Tokyo").startswith("2026-04-02T00:00:00")
