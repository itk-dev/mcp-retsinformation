import pytest
from unittest.mock import AsyncMock, MagicMock

from mcp_retsinformation.tools.search import (
    get_lovgivning,
    get_lovgivning_amendments,
    get_lovgivning_at_date,
    get_lovgivning_markdown,
    search_lovgivning,
)


@pytest.fixture
def mock_json_response():
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"id": 1, "title": "Test lov"}
    return response


@pytest.fixture
def mock_client(mocker, mock_json_response):
    client = MagicMock()
    client.get = AsyncMock(return_value=mock_json_response)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    mocker.patch("mcp_retsinformation.tools.search.httpx.AsyncClient", return_value=client)
    return client


# --- search_lovgivning ---

async def test_search_lovgivning_with_query(mock_client, mock_json_response):
    mock_json_response.json.return_value = [{"id": 1}, {"id": 2}]
    result = await search_lovgivning(search="skat", limit=5)
    mock_client.get.assert_called_once_with("/v1/lovgivning/", params={"limit": 5, "search": "skat"})
    assert result == [{"id": 1}, {"id": 2}]


async def test_search_lovgivning_without_query(mock_client, mock_json_response):
    mock_json_response.json.return_value = [{"id": 1}]
    result = await search_lovgivning(limit=3)
    mock_client.get.assert_called_once_with("/v1/lovgivning/", params={"limit": 3})
    assert result == [{"id": 1}]


async def test_search_lovgivning_default_limit(mock_client, mock_json_response):
    mock_json_response.json.return_value = []
    await search_lovgivning()
    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["limit"] == 10


# --- get_lovgivning ---

async def test_get_lovgivning(mock_client, mock_json_response):
    result = await get_lovgivning(year=2024, number=616)
    mock_client.get.assert_called_once_with("/v1/lovgivning/2024/616")
    assert result == mock_json_response.json.return_value


# --- get_lovgivning_markdown ---

async def test_get_lovgivning_markdown_no_filters(mock_client, mock_json_response):
    mock_json_response.text = "# Test lov\n\n§ 1..."
    result = await get_lovgivning_markdown(year=2024, number=616)
    mock_client.get.assert_called_once_with("/v1/lovgivning/2024/616/markdown", params={})
    assert result == "# Test lov\n\n§ 1..."


async def test_get_lovgivning_markdown_with_exclude(mock_client, mock_json_response):
    mock_json_response.text = "# Test lov"
    await get_lovgivning_markdown(year=2024, number=616, exclude="preamble,signature")
    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["exclude"] == "preamble,signature"


async def test_get_lovgivning_markdown_with_paragraphs(mock_client, mock_json_response):
    mock_json_response.text = "§ 1..."
    await get_lovgivning_markdown(year=2024, number=616, paragraphs="1-5")
    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["paragraphs"] == "1-5"


# --- get_lovgivning_at_date ---

async def test_get_lovgivning_at_date(mock_client, mock_json_response):
    result = await get_lovgivning_at_date(year=2024, number=616, date="2025-01-01")
    mock_client.get.assert_called_once_with("/v1/lovgivning/2024/616/versions/at/2025-01-01")
    assert result == mock_json_response.json.return_value


# --- get_lovgivning_amendments ---

async def test_get_lovgivning_amendments(mock_client, mock_json_response):
    mock_json_response.json.return_value = [{"amendment_id": 42}]
    result = await get_lovgivning_amendments(year=2024, number=616)
    mock_client.get.assert_called_once_with("/v1/lovgivning/2024/616/amendments")
    assert result == [{"amendment_id": 42}]
