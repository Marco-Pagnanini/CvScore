# Instructor notes

This file exists only in the `solution` branch.

## Branches

- `main`: the student version. `tools.py` has `read_cv` written as a worked example and one TODO, `compute_score` (Exercise 1), and `recruiter.py` is a stub (Assignment).
- `solution`: same as `main`, with `compute_score` in `tools.py` and `recruiter.py` complete. When you change `main`, merge `main` into `solution`.

The only other place to edit by hand is Exercise 2: in `cv_matcher.py` the last line is
`SYSTEM_PROMPT = VULNERABLE_PROMPT + RULES`. To switch to the safe prompt it becomes `SAFE_PROMPT + RULES`
(not `SAFE_PROMPT` alone: that would drop the verdict rules that make results repeatable).

## Answers to the recruiter's "to think about" questions

1. **Why receive the already extracted requirements instead of the raw job description?** The job description is text written
   by third parties and can contain marketing, noise or disguised instructions. The JD Analyst reduces it to structured
   requirements: the recruiter only works on data that has already been filtered, and its input has a known format.
2. **Would the score change if the recruiter wrote different questions?** No. The score is computed by `services/score.py` from
   the CV Matcher's `matches`; the recruiter sees neither the CV nor the verdicts, and its output never enters the formula.

## Bonus: questions about the weak points of the CV

The recruiter needs the requirements with verdict `no` or `partial`, that is the CV Matcher's `matches`. Change `orchestrator.py`:
step 4 of the prompt must send the `matches` (or only those with verdict `no`/`partial`) to the recruiter instead of the
requirements, and the recruiter's prompt must say how to use them. No other file changes.

## Checks before the lesson

- `docker compose exec backend python -m pytest -q` is green (6 tests). On `main` the two `compute_score` tests of `test_tools.py` are red until the student writes the tool: that is expected.
- With `test_data/cv_injected.pdf` and job description no. 6: vulnerable prompt versus safe prompt. Write down the real scores
  and compare them with the ones shown in the slides.
- A full analysis shows the Recruiter step in the log and the INTERVIEW QUESTIONS section in the result.
