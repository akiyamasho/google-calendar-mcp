.PHONY: dep run

dep:
	uv sync --dev

run:
	uv run google-calendar-mcp
