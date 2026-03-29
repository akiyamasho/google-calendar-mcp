from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def oauth_client_secret_file() -> Path:
    return Path(required_env("GOOGLE_OAUTH_CLIENT_SECRET_FILE")).expanduser().resolve()


def token_file() -> Path:
    raw = os.getenv("GOOGLE_CALENDAR_MCP_TOKEN_FILE", ".secrets/google-token.json").strip()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = project_root() / path
    return path.resolve()


def default_timezone() -> str:
    return os.getenv("GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE", "UTC").strip() or "UTC"


def maps_api_key() -> str | None:
    value = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    return value or None

