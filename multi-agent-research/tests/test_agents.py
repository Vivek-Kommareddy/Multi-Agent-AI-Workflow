import pytest

from src.agents.analyst import AnalystAgent
from src.agents.base import Task
from src.agents.critic import CriticAgent
from src.agents.planner import PlannerAgent
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.orchestrator.state import SharedState
from src.tools.file_writer import FileWriterTool
from src.tools.summarizer import SummarizerTool
from src.tools.web_scraper import WebScraperTool
from src.tools.web_search import WebSearchTool


@pytest.mark.asyncio
async def test_planner_execute():
    result = await PlannerAgent([]).execute(Task("1", "AI topic"), SharedState())
    assert "subtasks" in result.output


@pytest.mark.asyncio
async def test_researcher_execute():
    agent = ResearcherAgent([WebSearchTool(), WebScraperTool(), SummarizerTool()])
    result = await agent.execute(Task("2", "AI topic"), SharedState())
    assert result.output["sources"]


@pytest.mark.asyncio
async def test_analyst_writer_critic_execute():
    shared = SharedState()
    analysis = await AnalystAgent([]).execute(Task("a", {"key_points": ["x", "y"]}), shared)
    draft = await WriterAgent([FileWriterTool()]).execute(Task("w", {"analysis": analysis.output}), shared)
    review = await CriticAgent([]).execute(Task("c", draft.output["report"]), shared)
    assert "score" in review.output
