from app.models.cv import RequirementMatch, Score

WEIGHT = {"must": 3, "nice": 1}
VALUE = {"yes": 1, "partial": 0.5, "no": 0}


def compute_score(matches: list[RequirementMatch]) -> Score:
    total = sum(WEIGHT[m.kind] for m in matches) or 1
    points = sum(WEIGHT[m.kind] * VALUE[m.verdict] for m in matches)

    def met(kind):
        return sum(1 for m in matches if m.kind == kind and m.verdict == "yes")

    def tot(kind):
        return sum(1 for m in matches if m.kind == kind)

    return Score(
        score=round(100 * points / total),
        must_met=met("must"), must_total=tot("must"),
        nice_met=met("nice"), nice_total=tot("nice"),
    )
