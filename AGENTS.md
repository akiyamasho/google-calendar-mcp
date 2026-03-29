# AGENTS.md

## Purpose

This repository provides a minimal Google Calendar MCP server for agent clients such as Codex, Claude Code, and Cursor.

## Working rules

- Prefer the four exposed MCP tools instead of direct code edits when testing behavior.
- Keep responses compact and structured for low token usage.
- Do not add delete functionality for calendar events unless explicitly requested.
- When editing this repository, keep the MCP surface small and stable.
- Always use `uv` for Python dependency management and execution.
- Always keep a `Makefile` with at least `make dep` and `make run`.
- Always use conventional commits in the form `<type>(<component>): <change>`.
- Example: `feat(mcp-tools): add edit calendar event tool`

## Typical workflow

1. Ensure the required environment variables are present.
2. Install dependencies with `make dep`.
3. Run the server with `make run`.
4. Authenticate once in the browser when prompted.
5. Use `list_events`, `create_event`, `update_event`, or `fill_missing_locations_from_title`.
