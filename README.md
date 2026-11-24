# CvScore

A small Agentic SOA for the lab: you upload a CV (PDF) and paste a job description, and a team of agents returns
a 0-100 score explained requirement by requirement, suggestions to improve the CV and questions for the job interview.

```
FastAPI (POST /api/analyze)
  └─ Orchestrator
       ├─ JD Analyst   → requirements ("must" / "nice")
       ├─ CV Matcher   → verdict yes / partial / no for each requirement (tool: read_cv)
       ├─ Evaluator    → score, summary, suggestions (tool: compute_score)
       └─ Recruiter    → interview questions
MCP server (/mcp) → services/cv.py (reads the PDF), services/score.py (the formula)
```

## Run it

You need Docker and an Anthropic API key.

```bash
cp .env.example .env        # then write your ANTHROPIC_API_KEY in the .env file
docker compose up -d --build
```

Open http://localhost:3000.

- Changes to `backend/app` reload by themselves when you save.
- Changes to the frontend need `docker compose up -d --build` again.
- Backend logs: `docker compose logs -f backend`.

## The lab, in order

| # | What you do | Where | How you know you are done |
|---|---|---|---|
| 1 | **Exercise 1**: write the MCP tool `compute_score` (`read_cv` is already written, as an example) | `backend/app/mcp_tools/tools.py` | `docker compose exec backend pytest tests/test_tools.py -q` is green and an analysis of a CV completes |
| 2 | **Exercise 2**: prompt injection, from `VULNERABLE_PROMPT` to `SAFE_PROMPT` | `backend/app/agents/cv_matcher.py` | With `test_data/cv_injected.pdf` the score changes between the two prompts |
| 3 | **Assignment**: write the `recruiter` agent | `backend/app/agents/recruiter.py` | The INTERVIEW QUESTIONS section appears in the result. Guide: `exercise_guide/Assignment/guideline_recruiter.md` |

The lab slides describe every step. If a change does not show up, the most common cause is the container still running
the old code: `docker compose up -d --build`.

## Test data

In `exercise_guide/test_data/`:

- `job_applications_test.md`: seven job descriptions to paste into the form (strong match, partial match, no match, only "must" requirements, minimal text, marketing noise).
- `cv_clean.pdf`: the CV of a junior web developer (HTML, CSS, a bit of JavaScript).
- `cv_injected.pdf`: the same CV with an "HR" note written in white on white: invisible to the eye, but read by the model.
  For Exercise 2 use it with job description no. 6 ("Junior Python developer, basic knowledge of Git").

The same CV and the same job description always return the same report (in-memory cache, cleared when the server restarts).

## Tests

```bash
docker compose exec backend pytest -q
```

`test_score.py` checks the score formula, `test_tools.py` checks the MCP tools of Exercise 1 (the `compute_score` tests fail until you write it).
