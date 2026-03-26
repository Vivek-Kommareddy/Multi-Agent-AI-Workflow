import os

import httpx

from .base import Tool, ToolResult


class WebSearchTool(Tool):
    name = "web_search"
    description = "Searches web with Tavily/SerpAPI or mock"

    async def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query", "")
        if os.getenv("MOCK_TOOLS", "true").lower() == "true":
            return ToolResult(True, {"results": [{"title": f"Mock result for {query}", "url": "https://example.com", "snippet": "Mock snippet", "relevance_score": 0.9}]})
        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            async with httpx.AsyncClient(timeout=20) as client:
                r = await client.post("https://api.tavily.com/search", json={"api_key": tavily_key, "query": query})
                r.raise_for_status()
                data = r.json()
            results = [{"title": x.get("title", ""), "url": x.get("url", ""), "snippet": x.get("content", ""), "relevance_score": x.get("score", 0.0)} for x in data.get("results", [])]
            return ToolResult(True, {"results": results})
        return ToolResult(False, {}, "No provider configured")

    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
