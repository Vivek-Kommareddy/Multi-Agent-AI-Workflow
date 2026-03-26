"""Create workflow programmatically."""

import asyncio

from src.orchestrator.workflow import Workflow


async def main() -> None:
    wf = Workflow({
        "name": "Programmatic Workflow",
        "steps": [
            {"id": "plan", "agent": "planner", "output": "task_plan"},
            {"id": "research", "agent": "researcher", "output": "research_findings"},
            {"id": "analyze", "agent": "analyst", "output": "analysis"},
            {"id": "write", "agent": "writer", "output": "draft_report"},
        ],
    })
    result = await wf.run(topic="AI in biotech")
    print(result.report)


if __name__ == "__main__":
    asyncio.run(main())
