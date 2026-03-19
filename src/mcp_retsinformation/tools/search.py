import httpx
from loguru import logger

from ..config import settings
from ..server import mcp


@mcp.tool()
async def search_lovgivning(
    search: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search Danish legislation (love, bekendtgørelser, lovbekendtgørelser, cirkulærer, vejledninger).

    Args:
        search: Free-text search query in Danish.
        limit: Maximum number of results to return.
    """
    params: dict = {"limit": limit}
    if search:
        params["search"] = search

    async with httpx.AsyncClient(base_url=settings.retsinformation_base_url) as client:
        logger.debug("Searching lovgivning: search={!r} limit={}", search, limit)
        response = await client.get("/v1/lovgivning/", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_lovgivning(year: int, number: int) -> dict:
    """Fetch the full text of a specific Danish law or regulation.

    Args:
        year: The year the law was passed (e.g. 2024).
        number: The law number for that year (e.g. 616).
    """
    async with httpx.AsyncClient(base_url=settings.retsinformation_base_url) as client:
        logger.debug("Fetching lovgivning: {}/{}", year, number)
        response = await client.get(f"/v1/lovgivning/{year}/{number}")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_lovgivning_markdown(
    year: int,
    number: int,
    exclude: str | None = None,
    paragraphs: str | None = None,
) -> str:
    """Fetch a Danish law or regulation as Markdown.

    Args:
        year: The year the law was passed.
        number: The law number for that year.
        exclude: Comma-separated sections to exclude, e.g. "preamble,signature".
        paragraphs: Paragraph range to include, e.g. "1-5".
    """
    params: dict = {}
    if exclude:
        params["exclude"] = exclude
    if paragraphs:
        params["paragraphs"] = paragraphs

    async with httpx.AsyncClient(base_url=settings.retsinformation_base_url) as client:
        logger.debug("Fetching markdown: {}/{}", year, number)
        response = await client.get(f"/v1/lovgivning/{year}/{number}/markdown", params=params)
        response.raise_for_status()
        return response.text


@mcp.tool()
async def get_lovgivning_at_date(year: int, number: int, date: str) -> dict:
    """Fetch a Danish law exactly as it appeared on a specific date (time travel).

    Args:
        year: The year the law was passed.
        number: The law number for that year.
        date: ISO 8601 date string, e.g. "2025-01-01".
    """
    async with httpx.AsyncClient(base_url=settings.retsinformation_base_url) as client:
        logger.debug("Fetching lovgivning {}/{} at {}", year, number, date)
        response = await client.get(f"/v1/lovgivning/{year}/{number}/versions/at/{date}")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_lovgivning_amendments(year: int, number: int) -> list[dict]:
    """List all amendments to a Danish law.

    Args:
        year: The year the law was passed.
        number: The law number for that year.
    """
    async with httpx.AsyncClient(base_url=settings.retsinformation_base_url) as client:
        logger.debug("Fetching amendments: {}/{}", year, number)
        response = await client.get(f"/v1/lovgivning/{year}/{number}/amendments")
        response.raise_for_status()
        return response.json()
