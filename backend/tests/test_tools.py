"""Exercise 1 check: the two MCP tools exist, are documented and do their job.

Run it with:  docker compose exec backend pytest tests/test_tools.py -q
"""
import asyncio
import json
from pathlib import Path

from mcp import Client

from app.mcp_server import mcp
from app.mcp_tools import tools  # noqa: F401  (importing the module registers the tools)
from app.services import cv as cv_service

CV_SAMPLE = Path(__file__).parent / "data" / "cv_clean.pdf"


async def _list_tools():
    async with Client(mcp) as client:
        return (await client.list_tools()).tools


async def _call(name: str, arguments: dict):
    async with Client(mcp) as client:
        return await client.call_tool(name, arguments)


def _text(result) -> str:
    return "\n".join(c.text for c in result.content if c.type == "text")


def test_tools_are_registered():
    names = {t.name for t in asyncio.run(_list_tools())}
    assert {"read_cv", "compute_score"} <= names, f"tools registered on the MCP server: {sorted(names)}"


def test_tools_have_a_description():
    # the model never reads your code: it only reads the docstring
    for t in asyncio.run(_list_tools()):
        assert t.description and t.description.strip(), f"{t.name} has no docstring"


def test_read_cv_returns_the_cv_text():
    cv_id = cv_service.save_cv(CV_SAMPLE.read_bytes())
    try:
        result = asyncio.run(_call("read_cv", {"cv_id": cv_id}))
    finally:
        cv_service.delete_cv(cv_id)
    assert not result.is_error
    assert "HTML" in _text(result)


def test_compute_score_applies_the_formula():
    matches = [
        {"requirement": "a", "kind": "must", "verdict": "yes", "evidence": "x"},
        {"requirement": "b", "kind": "must", "verdict": "no", "evidence": ""},
        {"requirement": "c", "kind": "nice", "verdict": "partial", "evidence": "y"},
    ]
    result = asyncio.run(_call("compute_score", {"matches": matches}))
    assert not result.is_error
    assert json.loads(_text(result))["score"] == 50  # (3 + 0 + 0.5) / 7
