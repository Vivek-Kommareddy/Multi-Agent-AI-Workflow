import asyncio
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.config import Settings
from src.orchestrator.workflow import Workflow

from .schemas import JobResponse, ResearchRequest, StatusResponse

router = APIRouter()
_jobs: dict[str, dict] = {}


async def _run_job(job_id: str, topic: str, workflow_name: str) -> None:
    wf = Workflow.from_yaml(f"workflows/{workflow_name}.yaml", Settings())
    _jobs[job_id]["status"] = "running"
    result = await wf.run(topic=topic)
    _jobs[job_id]["status"] = "completed"
    _jobs[job_id]["result"] = {"report": result.report, "artifacts": result.artifacts}
    _jobs[job_id]["events"] = wf.events
    _jobs[job_id]["log"] = wf.state.log


@router.post("/research", response_model=JobResponse)
async def start_research(req: ResearchRequest) -> JobResponse:
    if not Path(f"workflows/{req.workflow}.yaml").exists():
        raise HTTPException(404, "workflow not found")
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "queued", "events": [], "log": [], "result": None}
    asyncio.create_task(_run_job(job_id, req.topic, req.workflow))
    return JobResponse(job_id=job_id)


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str) -> StatusResponse:
    if job_id not in _jobs:
        raise HTTPException(404, "job not found")
    status = _jobs[job_id]["status"]
    progress = 100 if status == "completed" else 50 if status == "running" else 0
    return StatusResponse(job_id=job_id, status=status, progress=progress, log=_jobs[job_id].get("log", []))


@router.get("/results/{job_id}")
async def get_results(job_id: str) -> dict:
    if job_id not in _jobs:
        raise HTTPException(404, "job not found")
    return _jobs[job_id].get("result") or {"status": _jobs[job_id]["status"]}


@router.get("/workflows")
async def list_workflows() -> dict:
    return {"workflows": sorted([p.stem for p in Path("workflows").glob("*.yaml")])}


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
