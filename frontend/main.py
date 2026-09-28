import json
import logging
import os
import re
import uuid
from pathlib import Path

import google.auth
import google.auth.transport.requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Force Vertex AI & explicit credentials
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/config/Desktop/Session1/smart-chef/sa-key.json"

import sys
sys.path = [p for p in sys.path if p.rstrip("/") != "/config/Desktop/Session1/smart-chef"]
sys.path.insert(0, "/config/Desktop/Session1/quebec-voter-compass")

from app.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("quebec-voter-compass-frontend")

_A2A_DATAPART_RE = re.compile(
    r"</?(?:a2a_datapart_json|a2ui-json)>", re.DOTALL
)
_A2UI_TAG_RE = re.compile(
    r"<a2ui-json>(.*?)</a2ui-json>", re.DOTALL
)
_A2A_TAG_RE = re.compile(
    r"<a2a_datapart_json>(.*?)</a2a_datapart_json>", re.DOTALL
)

app = FastAPI(title="Quebec Voter Compass 2026 Frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = InMemoryRunner(agent=root_agent)

@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    logger.exception("Error during request processing")
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "").strip()
    user_id = body.get("user_id") or "voter-user"

    if not message:
        return JSONResponse({"parts": [{"kind": "text", "text": "Please enter a question or topic."}]})

    # Fresh session for every turn to guarantee no context pollution
    session_id = str(uuid.uuid4())
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id=user_id, session_id=session_id
    )

    user_content = Content(role="user", parts=[Part(text=message)])

    parts: list[dict] = []

    async for event in runner.run_async(
        session_id=session_id,
        new_message=user_content,
        user_id=user_id,
    ):
        event_content = getattr(event, "content", None)
        logger.info(f"Event yielded: author={getattr(event, 'author', None)}, content={event_content}")
        if event_content and getattr(event_content, "parts", None):
            for p in event_content.parts:
                text_val = getattr(p, "text", None)
                if text_val:
                    # Check for <a2ui-json> tag format
                    u_matches = list(_A2UI_TAG_RE.finditer(text_val))
                    if u_matches:
                        for m in u_matches:
                            try:
                                parsed = json.loads(m.group(1).strip())
                                if isinstance(parsed, list):
                                    for item in parsed:
                                        parts.append({"kind": "a2ui", "data": item})
                                elif isinstance(parsed, dict):
                                    parts.append({"kind": "a2ui", "data": parsed})
                            except Exception:
                                pass
                        cleaned = _A2UI_TAG_RE.sub("", text_val).strip()
                        if cleaned:
                            parts.append({"kind": "text", "text": cleaned})
                    else:
                        a_matches = list(_A2A_TAG_RE.finditer(text_val))
                        if a_matches:
                            for m in a_matches:
                                try:
                                    env = json.loads(m.group(1))
                                    if isinstance(env, dict) and "data" in env:
                                        parts.append({"kind": "a2ui", "data": env["data"]})
                                except Exception:
                                    pass
                            cleaned = _A2A_TAG_RE.sub("", text_val).strip()
                            if cleaned:
                                parts.append({"kind": "text", "text": cleaned})
                        else:
                            # Try parsing bare JSON if text_val looks like A2UI JSON (even in markdown codeblock)
                            stripped = text_val.strip()
                            if stripped.startswith("```"):
                                stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
                                stripped = re.sub(r"\s*```$", "", stripped).strip()
                            if (stripped.startswith("[") or stripped.startswith("{")) and ("components" in stripped or "surfaceId" in stripped):
                                try:
                                    parsed = json.loads(stripped)
                                    if isinstance(parsed, list):
                                        for item in parsed:
                                            parts.append({"kind": "a2ui", "data": item})
                                    elif isinstance(parsed, dict):
                                        parts.append({"kind": "a2ui", "data": parsed})
                                except Exception:
                                    parts.append({"kind": "text", "text": text_val})
                            else:
                                parts.append({"kind": "text", "text": text_val})

                inline_data = getattr(p, "inline_data", None)
                if inline_data and getattr(inline_data, "data", None):
                    raw_bytes = inline_data.data
                    txt = raw_bytes.decode("utf-8", errors="ignore")
                    matches = list(_A2A_DATAPART_RE.finditer(txt))
                    if matches:
                        for m in matches:
                            try:
                                env = json.loads(m.group(1))
                                if isinstance(env, dict) and "data" in env:
                                    parts.append({"kind": "a2ui", "data": env["data"]})
                            except Exception:
                                pass
                    elif txt.strip():
                        parts.append({"kind": "text", "text": txt.strip()})

    if not parts:
        parts = [{"kind": "text", "text": "I checked the platforms for that issue. Please try selecting one of the prompt chips above or ask about Health Care, Cost of Living, Education, Child Care, Economy, or Environment."}]

    return JSONResponse({"parts": parts})

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
