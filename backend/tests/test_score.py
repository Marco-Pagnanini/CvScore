from app.models.cv import RequirementMatch
from app.services.score import compute_score


def m(kind, verdict):
    return RequirementMatch(requirement="x", kind=kind, verdict=verdict, evidence="")


def test_score_formula():
    s = compute_score([m("must", "yes"), m("must", "no"), m("nice", "partial")])
    assert s.score == 50  # (3 + 0 + 0.5) / 7
    assert (s.must_met, s.must_total, s.nice_met, s.nice_total) == (1, 2, 0, 1)


def test_empty():
    assert compute_score([]).score == 0
