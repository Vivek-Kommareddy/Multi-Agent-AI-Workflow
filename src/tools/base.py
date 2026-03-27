from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolResult:
    ok: bool
    data: dict
    error: str | None = None


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        ...

    @abstractmethod
    def get_schema(self) -> dict:
        ...
