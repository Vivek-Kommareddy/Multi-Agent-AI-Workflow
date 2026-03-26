from src.llm.prompts import SYSTEM_PROMPTS
from src.orchestrator.state import SharedState

from .base import Agent, Task


class CriticAgent(Agent):
    name = "critic"
    role = "Review and feedback"
    system_prompt = SYSTEM_PROMPTS["critic"]

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        report = str(task.content)
        issues = []
        if "## Sources" not in report:
            issues.append("Missing sources section")
        if len(report.split()) < 80:
            issues.append("Report is too short")
        score = max(1, 10 - 2 * len(issues))
        return {
            "score": score,
            "issues": issues,
            "suggestions": ["Expand evidence", "Improve conclusions"] if issues else [],
            "approved": score >= 7,
        }
