from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from src.agents.base import Task
from src.config import Settings

from .router import Router
from .scheduler import Scheduler
from .state import SharedState

# Project root is 3 levels up: workflow.py → orchestrator → src → project root
_PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class WorkflowResult:
    report: str
    artifacts: dict[str, Any]

    def save(self, path: str) -> None:
        Path(path).write_text(self.report, encoding="utf-8")


class Workflow:
    def __init__(self, definition: dict[str, Any], settings: Settings | None = None) -> None:
        self.definition = definition
        self.settings = settings or Settings()
        self.router = Router()
        self.scheduler = Scheduler()
        self.state = SharedState()
        self.events: list[dict[str, Any]] = []

    @classmethod
    def from_yaml(cls, path: str, settings: Settings | None = None) -> "Workflow":
        # Accept both absolute paths and paths relative to the project root
        p = Path(path)
        if not p.is_absolute():
            p = _PROJECT_ROOT / path
        return cls(yaml.safe_load(p.read_text(encoding="utf-8")), settings)

    async def _emit(self, event: str, payload: dict[str, Any]) -> None:
        self.events.append({"event": event, **payload})

    async def run(self, topic: str) -> WorkflowResult:
        # Use Any so that chained .get() calls on retrieved values are type-safe
        artifacts: dict[str, Any] = {"topic": topic}

        for step in self.definition.get("steps", []):
            sid: str = step["id"]

            if sid == "revise" and artifacts.get("review", {}).get("approved", True):
                continue

            await self._emit("step_started", {"step": sid})
            agent = self.router.get(step["agent"])

            payload: Any
            if sid == "plan":
                payload = topic
            elif sid == "research":
                subtasks: list[Any] = artifacts.get("task_plan", {}).get("subtasks", [])
                # Guard against empty subtasks list to avoid IndexError
                payload = subtasks[0]["task"] if subtasks else topic
            elif sid == "analyze":
                payload = artifacts.get("research_findings", {})
            elif sid == "write":
                payload = {
                    "analysis": artifacts.get("analysis", {}),
                    "sources": artifacts.get("research_findings", {}).get("sources", []),
                }
            elif sid == "review":
                payload = artifacts.get("draft_report", {}).get("report", "")
            elif sid == "revise":
                payload = {
                    "analysis": artifacts.get("analysis", {}),
                    "suggestions": artifacts.get("review", {}).get("suggestions", []),
                    "sources": artifacts.get("research_findings", {}).get("sources", []),
                }
            else:
                payload = artifacts

            # Capture loop variables explicitly so retries use the correct values
            _agent, _payload = agent, payload
            result = await self.scheduler.run_with_retry(
                lambda a=_agent, p=_payload: a.execute(Task(sid, p), self.state)
            )
            artifacts[step["output"]] = result.output
            await self._emit("step_finished", {"step": sid})

        report: str = (
            artifacts.get("final_report", artifacts.get("draft_report", {})).get("report", "")
        )
        return WorkflowResult(report=report, artifacts=artifacts)
