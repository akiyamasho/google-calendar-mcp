from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _dotenv_values() -> dict[str, str]:
    path = project_root() / ".env"
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            values[key] = value
    return values


def env(name: str, default: str | None = None) -> str | None:
    runtime = os.getenv(name)
    if runtime is not None and runtime.strip():
        return runtime.strip()

    dotenv_value = _dotenv_values().get(name)
    if dotenv_value is not None and dotenv_value.strip():
        return dotenv_value.strip()

    return default


def required_env(name: str) -> str:
    value = (env(name) or "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def oauth_client_secret_file() -> Path:
    return Path(required_env("GOOGLE_OAUTH_CLIENT_SECRET_FILE")).expanduser().resolve()


def token_file() -> Path:
    raw = (env("GOOGLE_CALENDAR_MCP_TOKEN_FILE", ".secrets/google-token.json") or "").strip()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = project_root() / path
    return path.resolve()


def default_timezone() -> str:
    return (env("GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE", "UTC") or "UTC").strip() or "UTC"


def maps_api_key() -> str | None:
    value = (env("GOOGLE_MAPS_API_KEY", "") or "").strip()
    return value or None
