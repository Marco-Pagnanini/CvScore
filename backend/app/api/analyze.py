import asyncio
import hashlib
import json

from fastapi import APIRouter, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.agents import orchestrator
from app.agents.runner import EVENTS
from app.models.cv import Report, RequirementMatch
from app.services import cv as cv_service
from app.services import score as score_service

router = APIRouter(prefix="/api")
MAX_PDF = 5 * 1024 * 1024
running: set[asyncio.Task] = set()  # keep task references so they are not garbage collected
# An LLM may answer differently each time (temperature cannot be set on this model), so the same CV + same job
# description must always return the same report: we compute it once and reuse it. Lost on restart.
CACHE: dict[str, dict] = {}


@router.post("/analyze")
async def analyze(cv: UploadFile, job_description: str = Form(min_length=20, max_length=10000)):
    data = await cv.read()
    if not data.startswith(b"%PDF") or len(data) > MAX_PDF:
        raise HTTPException(400, "A PDF of at most 5 MB is required")
    cv_id = cv_service.save_cv(data)
    queue: asyncio.Queue = asyncio.Queue()
    key = hashlib.sha256(data + job_description.encode()).hexdigest()

    async def work():
        EVENTS.set(queue)
        try:
            if key not in CACHE:
                text = await orchestrator.run_agent(f"cv_id: {cv_id}\n\nJob description:\n{job_description}")
                text = text.strip().removeprefix("```json").removesuffix("```")
                data = json.loads(text)
                # LLMs garble numbers when relaying them: recompute the score from the matches, deterministically.
                matches = [RequirementMatch.model_validate(m) for m in data["matches"]]
                data["score"] = score_service.compute_score(matches).model_dump()
                CACHE[key] = Report.model_validate(data).model_dump()
            await queue.put({"type": "result", "data": CACHE[key]})
        except Exception as e:
            await queue.put({"type": "error", "message": str(e)})
        finally:
            cv_service.delete_cv(cv_id)
            await queue.put(None)

    task = asyncio.create_task(work())
    running.add(task)
    task.add_done_callback(running.discard)

    async def events():
        while (event := await queue.get()) is not None:
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")
