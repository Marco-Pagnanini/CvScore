from app.agents.runner import run

SYSTEM_PROMPT = """You are the Job Description Analyst.
You receive a job description. Split it into a list of concrete, checkable requirements
(skills, experience, education, languages). Mark each one "must" (required) or "nice" (preferred, a plus).
Merge duplicates, skip company marketing text.
Reply ONLY with a JSON array of {"text": "...", "kind": "must"|"nice"}. No prose."""

ALLOWED_TOOLS: list[str] = []


async def run_agent(task: str) -> str:
    return await run("jd_analyst", SYSTEM_PROMPT, ALLOWED_TOOLS, task)
