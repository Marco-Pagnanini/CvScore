from app.agents.runner import run

# =====================================================================================
# EXERCISE: write the Recruiter agent
#
# Goal: given the requirements of a job, the Recruiter writes the questions a recruiter
# would ask a candidate in the job interview. They will appear in the UI, in a new
# "INTERVIEW QUESTIONS" section, as soon as this agent works.
#
# Until you finish, the app keeps working: run_agent() below returns an empty list "[]",
# so the Orchestrator gets no questions and the UI hides the section.
#
# How an agent is made (open jd_analyst.py: it is the same shape, and it also has no tools):
#   1. SYSTEM_PROMPT   who the agent is, what it receives, and EXACTLY what it must reply
#   2. ALLOWED_TOOLS   which MCP tools it may call (this agent needs none)
#   3. run_agent()     one call to run(...): the agent loop is already written in runner.py
#
# The Orchestrator already knows this agent (see orchestrator.py). It sends it the list of
# requirements found by the JD Analyst and puts your reply in the final JSON as "questions".
# So your reply MUST be a JSON array of strings, nothing else, for example:
#   ["Tell me about a project where you used FastAPI.", "How do you ..."]
#
# STEP 1  Write SYSTEM_PROMPT. Say: who it is, what it receives (job requirements, each
#         "must" or "nice"), how many questions (e.g. 5 to 8), how to order them
#         (must first), what to mix (technical + behavioural), and the reply format
#         ("Reply ONLY with a JSON array of strings. No prose.").
# STEP 2  Set ALLOWED_TOOLS: a list of tool names. Which ones does this agent need?
# STEP 3  Replace the placeholder return in run_agent() with the call to run(...).
#         Its first argument is the agent name shown in the live log: use "recruiter".
#
# HOW TO TEST
#   - Run the app, upload a CV, paste a job description (see exercise_guide/test_data).
#   - Done when the live log shows the "Recruiter" step finishing and the result page
#     shows a list of interview questions.
#   - If the app does not hot-reload your changes, stop it and start it again.
#   - Saving this file restarts the server and empties its memory of past analyses, so the same
#     CV + job description is analysed again from scratch: the score may differ slightly from your
#     previous run. This is normal LLM variability and has nothing to do with your agent.
# =====================================================================================

SYSTEM_PROMPT = ""  # STEP 1

ALLOWED_TOOLS: list[str] = []  # STEP 2


async def run_agent(task: str) -> str:
    return "[]"  # STEP 3: placeholder, replace it with the call to run(...)
