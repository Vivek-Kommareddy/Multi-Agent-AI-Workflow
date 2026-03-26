from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from src.agents.base import Task
from src.config import Settings

from .router import Router
from .scheduler import Scheduler
from .state import SharedState


@dataclass
class WorkflowResult:
    report: str
    artifacts: dict[str, object]

    def save(self, path: str) -> None:
        Path(path).write_text(self.report, encoding="utf-8")


class Workflow:
    def __init__(self, definition: dict, settings: Settings | None = None) -> None:
        self.definition = definition
        self.settings = settings or Settings()
        self.router = Router()
        self.scheduler = Scheduler()
        self.state = SharedState()
        self.events: list[dict[str, object]] = []

    @classmethod
    def from_yaml(cls, path: str, settings: Settings | None = None) -> "Workflow":
        return cls(yaml.safe_load(Path(path).read_text(encoding="utf-8")), settings)

    async def _emit(self, event: str, payload: dict[str, object]) -> None:
        self.events.append({"event": event, **payload})

    async def run(self, topic: str) -> WorkflowResult:
        artifacts: dict[str, object] = {"topic": topic}
        for step in self.definition.get("steps", []):
            sid = step["id"]
            if sid == "revise" and artifacts.get("review", {}).get("approved", True):
                continue
            await self._emit("step_started", {"step": sid})
            agent = self.router.get(step["agent"])
            if sid == "plan":
                payload = topic
            elif sid == "research":
                payload = artifacts.get("task_plan", {}).get("subtasks", [{"task": topic}])[0]["task"]
            elif sid == "analyze":
                payload = artifacts.get("research_findings", {})
            elif sid == "write":
                payload = {"analysis": artifacts.get("analysis", {}), "sources": artifacts.get("research_findings", {}).get("sources", [])}
            elif sid == "review":
                payload = artifacts.get("draft_report", {}).get("report", "")
            elif sid == "revise":
                payload = {"analysis": artifacts.get("analysis", {}), "suggestions": artifacts.get("review", {}).get("suggestions", [])}
            else:
                payload = artifacts
            result = await self.scheduler.run_with_retry(lambda: agent.execute(Task(sid, payload), self.state))
            artifacts[step["output"]] = result.output
            await self._emit("step_finished", {"step": sid})
        report = artifacts.get("final_report", artifacts.get("draft_report", {"report": ""})).get("report", "")
        return WorkflowResult(report=report, artifacts=artifacts)
