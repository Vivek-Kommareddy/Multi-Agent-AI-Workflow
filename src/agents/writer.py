from src.llm.prompts import SYSTEM_PROMPTS
from src.orchestrator.state import SharedState

from .base import Agent, Task


class WriterAgent(Agent):
    name = "writer"
    role = "Report writing"
    system_prompt = SYSTEM_PROMPTS["writer"]

    async def _perform(self, task: Task, context: SharedState) -> dict[str, object]:
        payload = task.content if isinstance(task.content, dict) else {"analysis": str(task.content)}
        analysis = payload.get("analysis", payload)
        lines = [
            "# Research Report",
            "## Executive Summary",
            "This report summarizes key findings from the workflow.",
            "## Key Findings",
        ]
        lines.extend([f"- {x}" for x in analysis.get("insights", [])])
        lines.append("## Detailed Analysis")
        lines.extend([f"- {x}" for x in analysis.get("comparisons", [])])
        lines.extend(["## Conclusions", "The evidence indicates key trends.", "## Sources"])
        lines.extend([f"- {s.get('title','Source')}: {s.get('url','')}" for s in payload.get("sources", [])])
        if payload.get("suggestions"):
            lines.extend(["## Revision Notes"] + [f"- {s}" for s in payload["suggestions"]])
        report = "\n".join(lines)
        await self.act("file_writer", path="outputs/final_report.md", content=report)
        return {"report": report}
