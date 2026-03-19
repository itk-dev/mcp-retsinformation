from .server import mcp
from .tools import search  # noqa: F401 — side-effect import registers tools on mcp


def main() -> None:
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
