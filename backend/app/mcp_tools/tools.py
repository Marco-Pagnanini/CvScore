from app.mcp_server import mcp
from app.models.cv import RequirementMatch, Score
from app.services import cv, score

# =====================================================================================
# EXERCISE 1: write the two MCP tools
#
# An MCP tool is a normal Python function that the agents can discover and call.
# The imports above are already there: you write the two functions.
# Each tool is the same four lines (see the slides):
#   - the decorator that registers the function on the MCP server (`mcp`)
#   - the signature, with type hints: they become the input/output schema of the tool
#   - a docstring: the model never reads your code, it only reads this sentence
#   - a body of one line, that calls the service (the logic stays in services/)
#
# HOW TO TEST
#   - docker compose exec backend pytest tests/test_tools.py -q   -> all green
#   - rebuild if needed (docker compose up -d --build), upload a CV and run an analysis:
#     if the agents find the tools, the analysis completes.
# =====================================================================================

# TODO 1: read_cv
#   input:  cv_id (str)
#   output: the plain text of the CV (str)
#   body:   call cv.read_cv_text(cv_id)


# TODO 2: compute_score
#   input:  matches (list[RequirementMatch])
#   output: Score
#   body:   call score.compute_score(matches)
