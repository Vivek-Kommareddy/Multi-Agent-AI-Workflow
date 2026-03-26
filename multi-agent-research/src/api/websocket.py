import asyncio

from fastapi import APIRouter, WebSocket

from .routes import _jobs

router = APIRouter()


@router.websocket("/ws/{job_id}")
async def ws_progress(websocket: WebSocket, job_id: str) -> None:
    await websocket.accept()
    sent = 0
    try:
        while True:
            job = _jobs.get(job_id)
            if not job:
                await websocket.send_json({"error": "job not found"})
                break
            events = job.get("events", [])
            while sent < len(events):
                await websocket.send_json(events[sent])
                sent += 1
            if job.get("status") == "completed":
                await websocket.send_json({"event": "done"})
                break
            await asyncio.sleep(0.3)
    finally:
        await websocket.close()
