import os

import httpx
from bs4 import BeautifulSoup

from .base import Tool, ToolResult


class WebScraperTool(Tool):
    name = "web_scraper"
    description = "Extract main content"

    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        if not url:
            return ToolResult(False, {}, "url required")
        if os.getenv("MOCK_TOOLS", "true").lower() == "true":
            return ToolResult(True, {"title": "Mock Page", "author": "Mock", "date": None, "text": "Mock content."})
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(url)
            resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for t in soup(["script", "style", "nav", "footer", "header", "aside"]):
            t.decompose()
        text = " ".join(soup.get_text(" ").split())
        return ToolResult(True, {"title": soup.title.string if soup.title else "", "author": None, "date": None, "text": text[:8000]})

    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}
