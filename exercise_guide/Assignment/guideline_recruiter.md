# Exercise: write the `recruiter` agent

**Goal:** complete the `recruiter` agent, which generates the questions a recruiter would ask a candidate in the job interview for the job description you enter.
The questions appear in the result page, in the **INTERVIEW QUESTIONS** section.

**What you learn**
- What an agent looks like: prompt + allowed tools + one call to `run(...)`.
- How to ask an LLM for an answer in a fixed format (a JSON array of strings).
- How the orchestrator uses a sub-agent without you touching anything else.

**Estimated time:** 10-15 minutes. **Files:** 1 modified (`backend/app/agents/recruiter.py`), about ten lines.

---

## What is already there

- The orchestrator, the `Report` model and the UI are already wired to the recruiter. **You only write `recruiter.py`.**
- Until you write it, the agent returns an empty list: the app works as before, the questions section does not appear and the "Recruiter" step in the live log stays grey.

---

## Step 0: start the app and see how it looks now

```bash
cp .env.example .env
```

Write your `ANTHROPIC_API_KEY` in the `.env` file, then:

```bash
docker compose up -d --build
```

Open http://localhost:3000, upload a PDF CV (for example `test_data/cv_clean.pdf`) and paste a job description (see `test_data/job_applications_test.md`).
The result does **not** contain the "INTERVIEW QUESTIONS" section.

---

## Step 1: read

Open `backend/app/agents/recruiter.py` and read the comments at the top: they explain the goal, the answer format and the 3 points to complete.
For an example of a complete agent without tools, look at `backend/app/agents/jd_analyst.py`.

---

## Step 2: write the 3 pieces

| Piece | What it must contain |
|---|---|
| `SYSTEM_PROMPT` | Who the agent is, what it receives (the job requirements, each one "must" or "nice"), how many questions to write, in what order, what kind of questions, and the exact format of the answer |
| `ALLOWED_TOOLS` | The list of MCP tools it may use. Does it need any? |
| `run_agent` | One call to `run(...)`: it replaces the temporary `return "[]"`. The first argument is the name shown in the live log |

---

## Step 3: try it

Save the file. The backend restarts by itself (if it does not: `docker compose restart backend`).
Run an analysis again.

**What you should see:**
- in the live log the **Recruiter** step lights up and then completes;
- the result shows the **INTERVIEW QUESTIONS** section with the questions, the first one about the most important requirement.

---

## If something goes wrong

| Symptom | Probable cause | Fix |
|---|---|---|
| No "INTERVIEW QUESTIONS" section | `run_agent` still returns the temporary value, or `SYSTEM_PROMPT` is empty | Check Step 2 again |
| Validation error on the result | The recruiter's answer is not a pure JSON array (there is text before or after it, or a code block) | Make the answer format more explicit in the prompt |
| The result arrives immediately and the agent log stays empty | Same CV and same job description as a previous run: the app reuses the saved result | Saving a file in `backend/app` restarts the server and clears it. Or change the CV or the job description |
| The score differs from the previous run | The server restarted and the LLM evaluated the CV from scratch: normal, unrelated to your agent | Nothing to do |

To see the backend errors: `docker compose logs -f backend`.

---

## To think about

1. The recruiter receives the requirements already extracted, not the raw job description. Why is that safer?
2. Would the score change if the recruiter wrote different questions? Why?

## Bonus

Make the questions target the weak points of the CV (the requirements with verdict `no` or `partial`).
What data does the recruiter need, and in which file do you have to change what the orchestrator passes to it?
