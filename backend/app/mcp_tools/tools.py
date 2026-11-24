from app.mcp_server import mcp
from app.models.cv import RequirementMatch, Score
from app.services import cv, score

# =====================================================================================
# EXERCISE 1 (SOLUTION): the MCP tool `compute_score`
#
# An MCP tool is a normal Python function that the agents can discover and call.
# The imports above are already there, and so is `read_cv`: it is your worked example.
# Read it first, then write `compute_score` in the same way.
#
# Each tool is the same four lines (see the slides):
#   - the decorator that registers the function on the MCP server (`mcp`)
#   - the signature, with type hints: they become the input/output schema of the tool
#   - a docstring: the model never reads your code, it only reads this sentence
#   - a body of one line, that calls the service (the logic stays in services/)
#
# HOW TO TEST
#   - docker compose exec backend pytest tests/test_tools.py -q   -> all green
#   - rebuild if needed (docker compose up -d --build), upload a CV and run an analysis:
#     if the Evaluator finds the tool, the analysis completes.
# =====================================================================================


# EXAMPLE (already written): read_cv
# The CV Matcher calls it to get the plain text of the CV.
@mcp.tool()
def read_cv(cv_id: str) -> str:
    """Return the plain text of the uploaded CV."""
    return cv.read_cv_text(cv_id)


# SOLUTION: compute_score
# The Evaluator calls it to turn the verdicts into a 0-100 score.
@mcp.tool()
def compute_score(matches: list[RequirementMatch]) -> Score:
    """Compute the 0-100 match score from the requirement verdicts."""
    return score.compute_score(matches)
