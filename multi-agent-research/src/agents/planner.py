from src.llm.prompts import SYSTEM_PROMPTS
from src.orchestrator.state import SharedState

from .base import Agent, Task


class PlannerAgent(Agent):
    name = "planner"
    role = "Task decomposition"
    system_prompt = SYSTEM_PROMPTS["planner"]

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        topic = str(task.content)
        subtasks = [
            {"id": "research", "task": f"Research key facts about {topic}", "agent": "researcher", "deps": []},
            {"id": "analyze", "task": "Analyze findings", "agent": "analyst", "deps": ["research"]},
            {"id": "write", "task": "Write report", "agent": "writer", "deps": ["analyze"]},
            {"id": "review", "task": "Review report", "agent": "critic", "deps": ["write"]},
        ]
        return {"topic": topic, "subtasks": subtasks}
