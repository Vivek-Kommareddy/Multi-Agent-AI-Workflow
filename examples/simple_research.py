"""Minimal example: research a topic and generate a report."""

import asyncio

from src.config import Settings
from src.orchestrator.workflow import Workflow


async def main() -> None:
    settings = Settings()
    workflow = Workflow.from_yaml("workflows/research_report.yaml", settings)
    result = await workflow.run(topic="The impact of AI on healthcare in 2024")
    print(result.report)
    result.save("outputs/healthcare_ai_report.md")


if __name__ == "__main__":
    asyncio.run(main())
