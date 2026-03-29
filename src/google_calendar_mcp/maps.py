from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"


@dataclass
class PlaceMatch:
    name: str
    formatted_address: str
    google_maps_uri: str | None

    def as_location(self) -> str:
        if self.google_maps_uri:
            return f"{self.formatted_address} ({self.google_maps_uri})"
        return self.formatted_address


def search_place_by_text(query: str, api_key: str) -> PlaceMatch | None:
    payload = json.dumps({"textQuery": query, "pageSize": 1}).encode("utf-8")
    request = Request(
        TEXT_SEARCH_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.googleMapsUri",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Google Maps lookup failed: {exc}") from exc

    places = data.get("places") or []
    if not places:
        return None

    place = places[0]
    display_name = (place.get("displayName") or {}).get("text") or query
    return PlaceMatch(
        name=display_name,
        formatted_address=place.get("formattedAddress") or display_name,
        google_maps_uri=place.get("googleMapsUri"),
    )

