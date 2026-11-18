from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analyze
from app.mcp_server import mcp
from app.mcp_tools import tools  # noqa: F401  (registers the MCP tools)

mcp_app = mcp.streamable_http_app(streamable_http_path="/mcp", stateless_http=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(title="CV Scoring", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
app.include_router(analyze.router)
app.mount("/", mcp_app)  # mounted last so FastAPI routes win
