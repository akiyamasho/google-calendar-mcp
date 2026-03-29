from google_calendar_mcp import config


def test_dotenv_is_used_when_runtime_env_is_missing(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "project_root", lambda: tmp_path)
    (tmp_path / ".env").write_text(
        "GOOGLE_OAUTH_CLIENT_SECRET_FILE=/tmp/client.json\n"
        "GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE=Asia/Tokyo\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("GOOGLE_OAUTH_CLIENT_SECRET_FILE", raising=False)
    monkeypatch.delenv("GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE", raising=False)

    assert config.oauth_client_secret_file().name == "client.json"
    assert config.default_timezone() == "Asia/Tokyo"


def test_runtime_env_overrides_dotenv(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "project_root", lambda: tmp_path)
    (tmp_path / ".env").write_text(
        "GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE=Asia/Tokyo\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE", "UTC")

    assert config.default_timezone() == "UTC"
