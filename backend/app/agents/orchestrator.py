from app.agents import cv_matcher, evaluator, jd_analyst, recruiter
from app.agents.runner import run

SYSTEM_PROMPT = """You are the Orchestrator of a CV scoring pipeline. You never judge the CV yourself.
1. Send the job description to jd_analyst -> get the requirements.
2. Send the requirements + cv_id to cv_matcher -> get the matches.
3. Send the matches to evaluator -> get score, summary, suggestions.
4. Send the requirements to recruiter -> get the interview questions.
Call one agent at a time. Pass each one a complete, self-contained task: it sees nothing else.
Final reply: ONLY one flat JSON object, no nesting of the evaluator reply:
{"matches": [...from cv_matcher], "score": <the "score" object from evaluator>, "summary": <evaluator summary>, "suggestions": <evaluator suggestions>, "questions": <recruiter reply>}. No prose."""

ALLOWED_TOOLS = ["jd_analyst", "cv_matcher", "evaluator", "recruiter"]
SUB_AGENTS = {"jd_analyst": jd_analyst.run_agent, "cv_matcher": cv_matcher.run_agent,
              "evaluator": evaluator.run_agent, "recruiter": recruiter.run_agent}


async def run_agent(task: str) -> str:
    return await run("orchestrator", SYSTEM_PROMPT, ALLOWED_TOOLS, task, sub_agents=SUB_AGENTS)
