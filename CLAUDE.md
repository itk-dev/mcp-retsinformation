# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`mcp-retsinformation` is a [FastMCP](https://github.com/jlowin/fastmcp) server that exposes tools for querying Danish legislation via the [retsinformation-api.dk](https://retsinformation-api.dk) REST API (`https://retsinformation-api.dk/v1/lovgivning/`). The API is free, requires no authentication, but is rate-limited to 20 req/hour and 50 req/day per IP.

## Commands

Use [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies (creates .venv)
uv sync --extra dev

# Run the MCP server (stdio transport, for local development)
python -m mcp_retsinformation

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_search.py

# Build and run with Docker (dev profile mounts source for live reload)
docker compose --profile dev up --build

# Build and run in production mode
docker compose --profile prod up --build
```

## Architecture

```
src/mcp_retsinformation/
├── server.py        # Creates the single FastMCP instance (`mcp`)
├── main.py          # Entry point: imports tools (triggering registration), calls mcp.run()
├── __main__.py      # Allows `python -m mcp_retsinformation`
├── config.py        # Pydantic Settings — loads from .env
└── tools/
    └── search.py    # @mcp.tool()-decorated functions registered on the mcp instance
```

**Tool registration pattern:** `server.py` creates the `mcp = FastMCP(...)` instance. Each file in `tools/` imports `mcp` from `server.py` and decorates functions with `@mcp.tool()`. `main.py` imports the tools modules as side-effect imports to trigger registration before calling `mcp.run()`.

**Transport:** The server runs with `streamable-http` transport on port 8000 when deployed via Docker. For local Claude Desktop integration, run with the default `stdio` transport by omitting the `transport` argument.

## Configuration

Copy `.env.example` to `.env`. Currently the only setting is `RETSINFORMATION_BASE_URL` (defaults to `https://api.retsinformation.dk`).
