"""Web chat UI + API — same agent-core tools as the MCP server, different transport.

FastAPI serves a minimal chat page and an SSE endpoint that runs the agent loop.
Sessions are kept in memory keyed by session_id (MVP; swap for SQLite when multi-user).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Runnable as a plain script even without `pip install -e .`.
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "packages"))

from fastapi import FastAPI  # noqa: E402
from fastapi.responses import HTMLResponse, StreamingResponse  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from agent_core import config, loop  # noqa: E402

app = FastAPI(title="Work Agent")
_SESSIONS: dict[str, list] = {}
_STATIC = Path(__file__).resolve().parent / "static"


class ChatIn(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((_STATIC / "index.html").read_text(encoding="utf-8"))


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "provider": loop.provider(), "agent": config.agent_name()}


@app.post("/api/chat")
def chat(body: ChatIn) -> StreamingResponse:
    history = _SESSIONS.setdefault(body.session_id, [])
    history.append({"role": "user", "content": body.message})

    def gen():
        for event in loop.run_turn(history):
            if event.get("type") == "history":
                _SESSIONS[body.session_id] = event["messages"]
                continue
            yield f"data: {json.dumps(event, default=str)}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8765)
