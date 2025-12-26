from rragent.schema import TraceEvent
from rragent.agents.parser_agent import parse_jd_and_resumes
from rragent.agents.matcher_agent import match_and_score
from rragent.agents.evidence_agent import attach_evidence
from rragent.agents.fairness_agent import fairness_check
from rragent.agents.narrator_agent import narrate

def run_pipeline(jd_text: str, candidates: list[dict], weights: dict) -> dict:
    trace: list[TraceEvent] = []

    jd_struct, cand_struct, ev = parse_jd_and_resumes(jd_text, candidates)
    trace.append(ev)

    scored, ev = match_and_score(jd_struct, cand_struct, weights)
    trace.append(ev)

    scored, ev = attach_evidence(jd_struct, scored)
    trace.append(ev)

    scored, ev = fairness_check(scored)
    trace.append(ev)

    ranked, ev = narrate(jd_struct, scored)
    trace.append(ev)

    trace_dicts = [t.to_dict() for t in trace]
    return {"ranked": ranked, "trace": trace_dicts}
