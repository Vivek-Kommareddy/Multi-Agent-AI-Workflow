from pydantic import BaseModel


class ResearchRequest(BaseModel):
    topic: str
    workflow: str = "research_report"


class JobResponse(BaseModel):
    job_id: str


class StatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    log: list[dict]
