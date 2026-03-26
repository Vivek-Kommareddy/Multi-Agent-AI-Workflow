from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.memory.conversation import ConversationMemory
from src.orchestrator.state import SharedState
from src.tools.base import Tool, ToolResult


@dataclass
class Task:
    id: str
    content: object
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class AgentResult:
    task_id: str
    agent: str
    output: dict[str, object]
    reflection: str


class Agent(ABC):
    name: str
    role: str
    system_prompt: str

    def __init__(self, tools: list[Tool] | None = None, memory: ConversationMemory | None = None) -> None:
        self.tools = tools or []
        self.memory = memory or ConversationMemory()

    async def execute(self, task: Task, context: SharedState) -> AgentResult:
        thought = await self.think(task)
        await context.append_log(self.name, "think", thought)
        output = await self._perform(task, context)
        result = AgentResult(task.id, self.name, output, "")
        result.reflection = await self.reflect(result)
        await context.append_log(self.name, "reflect", result.reflection)
        return result

    async def think(self, task: Task) -> str:
        t = f"Thinking about: {task.content}"
        self.memory.add("assistant", t)
        return t

    async def act(self, action: str, **kwargs) -> ToolResult:
        for tool in self.tools:
            if tool.name == action:
                return await tool.execute(**kwargs)
        return ToolResult(False, {}, f"Tool {action} not found")

    async def reflect(self, result: AgentResult) -> str:
        return f"Completed {result.task_id}"

    @abstractmethod
    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        ...
