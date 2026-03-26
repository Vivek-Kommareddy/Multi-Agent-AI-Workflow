import pytest

from src.tools.calculator import CalculatorTool
from src.tools.summarizer import SummarizerTool
from src.tools.web_scraper import WebScraperTool
from src.tools.web_search import WebSearchTool


@pytest.mark.asyncio
async def test_web_search_mock():
    result = await WebSearchTool().execute(query="ai")
    assert result.ok and result.data["results"]


@pytest.mark.asyncio
async def test_web_scraper_mock():
    result = await WebScraperTool().execute(url="https://example.com")
    assert result.ok and "text" in result.data


@pytest.mark.asyncio
async def test_calculator():
    result = await CalculatorTool().execute(expression="2+3*4")
    assert result.data["value"] == 14


@pytest.mark.asyncio
async def test_summarizer():
    result = await SummarizerTool().execute(text="one two three", target_length=2)
    assert result.ok
