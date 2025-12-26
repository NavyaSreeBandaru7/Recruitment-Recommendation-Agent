from rragent.schema import TraceEvent
from rragent.utils.scoring import score_candidate

def match_and_score(jd_struct: dict, cand_struct: list[dict], weights: dict):
    scored = []
    for c in cand_struct:
        s = score_candidate(jd_struct["items"], c["text"], weights)
        scored.append({**c, **s})

    scored.sort(key=lambda x: x["score_total"], reverse=True)
    for i, row in enumerate(scored, start=1):
        row["rank"] = i

    ev = TraceEvent(
        step="2",
        agent="MatcherAgent",
        status="ok",
        summary="Scored candidates using weighted matching (skills/resp/exp/other) and ranked them.",
        details=str(weights)
    )
    return scored, ev
