from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from google_calendar_mcp.config import (
    default_timezone,
    maps_api_key,
    oauth_client_secret_file,
    token_file,
)
from google_calendar_mcp.google_api import calendar_service
from google_calendar_mcp.maps import search_place_by_text
from google_calendar_mcp.models import (
    compact_event,
    event_time_fields,
    normalize_time_max,
    normalize_time_min,
)


mcp = FastMCP("google-calendar", json_response=True)


def _service():
    return calendar_service(oauth_client_secret_file(), token_file())


def _calendar_get(calendar_id: str, event_id: str) -> dict[str, Any]:
    return _service().events().get(calendarId=calendar_id, eventId=event_id).execute()


@mcp.tool()
def list_events(
    start: str,
    end: str,
    calendar_id: str = "primary",
    query: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """List events in a date/time range with a compact payload."""
    service = _service()
    response = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=normalize_time_min(start, default_timezone()),
            timeMax=normalize_time_max(end, default_timezone()),
            q=query or None,
            singleEvents=True,
            orderBy="startTime",
            maxResults=min(max(limit, 1), 250),
        )
        .execute()
    )
    events = [compact_event(item) for item in response.get("items", [])]
    return {"calendar_id": calendar_id, "count": len(events), "events": events}


@mcp.tool()
def create_event(
    title: str,
    start: str,
    end: str,
    calendar_id: str = "primary",
    timezone: str | None = None,
    location: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Create a calendar event."""
    start_fields, end_fields = event_time_fields(start, end, timezone or default_timezone())
    body: dict[str, Any] = {"summary": title, "start": start_fields, "end": end_fields}
    if location:
        body["location"] = location
    if description:
        body["description"] = description

    created = _service().events().insert(calendarId=calendar_id, body=body).execute()
    return {"created": compact_event(created)}


@mcp.tool()
def update_event(
    event_id: str,
    calendar_id: str = "primary",
    title: str | None = None,
    start: str | None = None,
    end: str | None = None,
    timezone: str | None = None,
    location: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Update selected fields of an existing event. This tool never deletes events."""
    event = _calendar_get(calendar_id, event_id)

    if title is not None:
        event["summary"] = title
    if description is not None:
        event["description"] = description
    if location is not None:
        event["location"] = location
    if start is not None or end is not None:
        current_start = (event.get("start") or {}).get("dateTime") or (event.get("start") or {}).get("date")
        current_end = (event.get("end") or {}).get("dateTime") or (event.get("end") or {}).get("date")
        start_fields, end_fields = event_time_fields(
            start or current_start,
            end or current_end,
            timezone or default_timezone(),
        )
        event["start"] = start_fields
        event["end"] = end_fields

    updated = _service().events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    return {"updated": compact_event(updated)}


@mcp.tool()
def fill_missing_locations_from_title(
    start: str,
    end: str,
    calendar_id: str = "primary",
    limit: int = 50,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Search Google Maps using each title and add a location only when the event has none."""
    api_key = maps_api_key()
    if not api_key:
        raise ValueError("Missing GOOGLE_MAPS_API_KEY")

    listed = list_events(start=start, end=end, calendar_id=calendar_id, limit=limit)
    updated_events: list[dict[str, Any]] = []
    skipped = 0

    for item in listed["events"]:
        if item.get("location") or not item.get("title"):
            skipped += 1
            continue

        match = search_place_by_text(item["title"], api_key)
        if not match:
            skipped += 1
            continue

        if dry_run:
            updated_events.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "suggested_location": match.as_location(),
                }
            )
            continue

        updated = update_event(
            event_id=item["id"],
            calendar_id=calendar_id,
            location=match.as_location(),
        )
        updated_events.append(updated["updated"])

    return {
        "calendar_id": calendar_id,
        "dry_run": dry_run,
        "updated_count": len(updated_events),
        "skipped_count": skipped,
        "events": updated_events,
    }
def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
