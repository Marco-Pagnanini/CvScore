from typing import Literal

from pydantic import BaseModel


class Requirement(BaseModel):
    text: str
    kind: Literal["must", "nice"]


class RequirementMatch(BaseModel):
    requirement: str
    kind: Literal["must", "nice"]
    verdict: Literal["yes", "partial", "no"]
    evidence: str  # CV sentence that proves it ("" when verdict is no)


class Score(BaseModel):
    score: int  # 0-100
    must_met: int
    must_total: int
    nice_met: int
    nice_total: int


class Report(BaseModel):
    matches: list[RequirementMatch]
    score: Score
    summary: str
    suggestions: list[str]
