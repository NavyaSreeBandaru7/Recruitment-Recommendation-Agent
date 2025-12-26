from rragent.schema import TraceEvent
from rragent.utils.text import best_snippet

def attach_evidence(jd_struct: dict, scored: list[dict]):
    jd_items = jd_struct["items"]
    for c in scored:
        evidence = []
        for item in jd_items[:20]:
            snip = best_snippet(c["text"], item)
            if snip:
                evidence.append({"jd_item": item[:90], "resume_snippet": snip})
        c["evidence"] = evidence

    ev = TraceEvent(
        step="3",
        agent="EvidenceAgent",
        status="ok",
        summary="Attached supporting resume snippets for top JD items (evidence-first explanations)."
    )
    return scored, ev
