from urllib.parse import urlparse

from src.llm.prompts import SYSTEM_PROMPTS
from src.orchestrator.state import SharedState

from .base import Agent, Task


class ResearcherAgent(Agent):
    name = "researcher"
    role = "Web research"
    system_prompt = SYSTEM_PROMPTS["researcher"]

    def _credibility(self, url: str) -> float:
        d = urlparse(url).netloc.lower()
        if d.endswith(".gov") or d.endswith(".edu"):
            return 0.95
        if d.endswith(".org") or d.endswith(".com"):
            return 0.75
        return 0.5

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        res = await self.act("web_search", query=str(task.content))
        hits = res.data.get("results", []) if res.ok else []
        key_points, sources, raw_data = [], [], []
        for hit in hits[:5]:
            scrape = await self.act("web_scraper", url=hit["url"])
            text = scrape.data.get("text", hit.get("snippet", "")) if scrape.ok else hit.get("snippet", "")
            summ = await self.act("summarizer", text=text, target_length=40, mode="extractive")
            key_points.append(summ.data.get("summary", ""))
            sources.append({"title": hit.get("title"), "url": hit.get("url"), "credibility": self._credibility(hit.get("url", ""))})
            raw_data.append({"result": hit, "content": text[:500]})
        return {"topic": str(task.content), "key_points": key_points, "sources": sources, "raw_data": raw_data}
