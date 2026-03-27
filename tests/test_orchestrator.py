import pytest

from src.orchestrator.workflow import Workflow


@pytest.mark.asyncio
async def test_workflow_runs():
    workflow = Workflow.from_yaml("workflows/research_report.yaml")
    result = await workflow.run("AI in healthcare")
    assert result.report.startswith("# Research Report")
    assert workflow.events
