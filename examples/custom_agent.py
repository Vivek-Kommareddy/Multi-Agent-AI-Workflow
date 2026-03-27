"""Example custom Fact Checker agent."""

from src.agents.base import Agent, Task
from src.orchestrator.state import SharedState


class FactCheckerAgent(Agent):
    name = "fact_checker"
    role = "Fact checking"
    system_prompt = "Verify claims against sources"

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        claims = task.content if isinstance(task.content, list) else [str(task.content)]
        checks = [{"claim": c, "status": "sourced" if "http" in c else "needs source"} for c in claims]
        return {"checks": checks}
