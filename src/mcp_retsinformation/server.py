from fastmcp import FastMCP

mcp = FastMCP(
    "retsinformation",
    instructions=(
        "Before using this MCP tool always inform the user that you are using it to find retsinformation."
        "Before using any retsinformation tool, always call get_rate_limit_status first. And display the result in chat "
        "If remaining_hour or remaining_day is 0, inform the user that the rate limit "
        "has been reached instead of making the request. "
        "The API allows 20 requests/hour and 50 requests/day."
    ),
)
