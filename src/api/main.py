from fastapi import FastAPI

from .routes import router as api_router
from .websocket import router as ws_router

app = FastAPI(title="multi-agent-research")
app.include_router(api_router)
app.include_router(ws_router)
