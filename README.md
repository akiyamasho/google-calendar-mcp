# google-calendar-mcp

A very small stdio MCP server for Google Calendar. It is optimized for agent use:

- low-token event payloads
- query, add, and edit calendar events
- no delete tool
- optional Google Maps location enrichment for events missing `location`

## Tools

1. `list_events`
2. `create_event`
3. `update_event`
4. `fill_missing_locations_from_title`

All tools default to `calendar_id="primary"` and return compact JSON.

## Google setup

1. Create a Google Cloud project.
2. Enable `Google Calendar API`.
3. If you want location enrichment, enable `Places API (New)`.
4. Create an OAuth client for a desktop app.
5. Download the OAuth client JSON.

## Environment

Required:

- `GOOGLE_OAUTH_CLIENT_SECRET_FILE=/absolute/path/to/client_secret.json`

Optional:

- `GOOGLE_CALENDAR_MCP_TOKEN_FILE=.secrets/google-token.json`
- `GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE=Asia/Tokyo`
- `GOOGLE_MAPS_API_KEY=...`

The first authenticated run opens a browser and stores the refresh token in `.secrets/google-token.json` by default.

You can put these in a repo-local `.env` file. Real environment variables still win over `.env`.

Example:

```dotenv
GOOGLE_OAUTH_CLIENT_SECRET_FILE=/absolute/path/to/client_secret.json
GOOGLE_CALENDAR_MCP_TOKEN_FILE=.secrets/google-token.json
GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE=Asia/Tokyo
GOOGLE_MAPS_API_KEY=
```

## Run with uv

```bash
uv run google-calendar-mcp
```

## Make targets

```bash
make dep
make run
```

## MCP setup

### Generic JSON

Use this shape in any MCP client that accepts `command`, `args`, and `env`:

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/google-calendar-mcp",
        "run",
        "google-calendar-mcp"
      ],
      "env": {
        "GOOGLE_OAUTH_CLIENT_SECRET_FILE": "/absolute/path/to/client_secret.json",
        "GOOGLE_CALENDAR_MCP_TOKEN_FILE": "/absolute/path/to/google-calendar-mcp/.secrets/google-token.json",
        "GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE": "Asia/Tokyo",
        "GOOGLE_MAPS_API_KEY": "optional-for-location-enrichment"
      }
    }
  }
}
```

If `.env` exists in this repository, you can omit most or all of the `env` block above.

### Codex

```bash
codex mcp add google-calendar --env GOOGLE_OAUTH_CLIENT_SECRET_FILE=/absolute/path/to/client_secret.json --env GOOGLE_CALENDAR_MCP_TOKEN_FILE=/absolute/path/to/google-calendar-mcp/.secrets/google-token.json --env GOOGLE_CALENDAR_MCP_DEFAULT_TIMEZONE=Asia/Tokyo -- uv --directory /absolute/path/to/google-calendar-mcp run google-calendar-mcp
```

### Claude Code / Cursor

Use the generic JSON block above in the client's MCP config.

## Process model

This is already a stdio server. It does not need to run as a long-lived daemon.

- The MCP client launches it on demand with `uv --directory /path/to/repo run google-calendar-mcp`
- The server handles the stdio session
- The process exits when the client closes the session

You only need a permanently running process if you choose to wrap it in one yourself, which is not required here.

## Example agent request

```text
Go through all my events in my authenticated Google Account from 2026-04-01 to 2026-04-30 and add Google Maps locations based on the title only if the location is not set yet.
```

The agent should call `fill_missing_locations_from_title`.

## Notes

- Datetimes should be ISO 8601 strings.
- Dates like `2026-04-01` are treated as all-day dates.
- The location enrichment tool only updates events that do not already have a location.
- Google Maps lookups use the event title as the only search query.
