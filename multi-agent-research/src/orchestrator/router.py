from src.agents.analyst import AnalystAgent
from src.agents.critic import CriticAgent
from src.agents.planner import PlannerAgent
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.tools.calculator import CalculatorTool
from src.tools.file_writer import FileWriterTool
from src.tools.summarizer import SummarizerTool
from src.tools.web_scraper import WebScraperTool
from src.tools.web_search import WebSearchTool


class Router:
    def __init__(self) -> None:
        self._agents = {
            "planner": PlannerAgent([]),
            "researcher": ResearcherAgent([WebSearchTool(), WebScraperTool(), SummarizerTool()]),
            "analyst": AnalystAgent([CalculatorTool(), SummarizerTool()]),
            "writer": WriterAgent([FileWriterTool()]),
            "critic": CriticAgent([]),
        }

    def get(self, name: str):
        if name not in self._agents:
            raise KeyError(name)
        return self._agents[name]
