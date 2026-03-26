import asyncio

from fastapi.testclient import TestClient

from src.api.main import app


def test_api_health_and_workflows():
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert "research_report" in client.get("/workflows").json()["workflows"]


def test_api_research_lifecycle():
    client = TestClient(app)
    job_id = client.post("/research", json={"topic": "AI", "workflow": "research_report"}).json()["job_id"]
    for _ in range(40):
        status = client.get(f"/status/{job_id}").json()
        if status["status"] == "completed":
            break
        asyncio.run(asyncio.sleep(0.1))
    results = client.get(f"/results/{job_id}").json()
    assert "report" in results
