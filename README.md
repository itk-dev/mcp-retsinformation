# mcp-retsinformation

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants (Claude, etc.) direct access to Danish legislation via [retsinformation-api.dk](https://retsinformation-api.dk).

Once connected, an AI can search for laws, read their full text, inspect amendment history, and retrieve how a law looked on any given date in the past.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Task](https://taskfile.dev/installation/)

## Getting started

```bash
cp .env.example .env
task dev
```

This builds the image and starts the dev container with the source directory mounted.

## Available tools

| Tool | Description | Test coverage |
|---|---|---|
| `search_lovgivning` | Search across all document types by free text | with query, without query, default limit |
| `get_lovgivning` | Fetch the full structured text of a law by year and number | correct URL and return value |
| `get_lovgivning_markdown` | Fetch a law as Markdown, with optional section filtering | no filters, with `exclude`, with `paragraphs` |
| `get_lovgivning_at_date` | Retrieve a law exactly as it appeared on a specific date | correct URL with date |
| `get_lovgivning_amendments` | List all amendments made to a law | correct URL and return value |

## Testing

Run the full test suite:

```bash
task test
```

Run a single file:

```bash
task test:file FILE=tests/test_search.py
```

## All tasks

```
task install      Install dependencies incl. dev extras
task run          Run the MCP server (stdio transport)
task test         Run all tests
task test:file    Run a single test file (FILE=...)
task dev          Build and start the dev container
task prod         Build and start the production container
task down         Stop and remove containers
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `RETSINFORMATION_BASE_URL` | `https://retsinformation-api.dk` | Base URL for the API |

The API is free, requires no authentication, and is rate-limited to 20 requests/hour and 50 requests/day per IP.

## Connecting to Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "retsinformation": {
      "command": "docker",
      "args": ["compose", "run", "--rm", "app-dev", "python", "-m", "mcp_retsinformation"]
    }
  }
}
```
