from app.mcp_server import mcp
from app.models.cv import RequirementMatch, Score
from app.services import cv, score


@mcp.tool()
def read_cv(cv_id: str) -> str:
    """Return the plain text of the uploaded CV."""
    return cv.read_cv_text(cv_id)


@mcp.tool()
def compute_score(matches: list[RequirementMatch]) -> Score:
    """Compute the 0-100 match score from the requirement verdicts."""
    return score.compute_score(matches)
