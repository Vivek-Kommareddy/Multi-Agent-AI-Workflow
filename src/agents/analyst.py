from src.llm.prompts import SYSTEM_PROMPTS
from src.orchestrator.state import SharedState

from .base import Agent, Task


class AnalystAgent(Agent):
    name = "analyst"
    role = "Data analysis"
    system_prompt = SYSTEM_PROMPTS["analyst"]

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        findings = task.content if isinstance(task.content, dict) else {"key_points": [str(task.content)]}
        points = findings.get("key_points", [])
        return {
            "insights": [f"Insight {i+1}: {p[:120]}" for i, p in enumerate(points[:5])],
            "data_points": points,
            "comparisons": [f"Compare: {points[0][:40]} <> {points[1][:40]}"] if len(points) >= 2 else [],
            "gaps": ["Need quantitative validation", "Need counterarguments"] if points else ["No findings"],
        }
