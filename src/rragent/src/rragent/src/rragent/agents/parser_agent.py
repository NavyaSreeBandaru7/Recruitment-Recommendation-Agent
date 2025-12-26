from rragent.schema import TraceEvent
from rragent.utils.text import normalize_text, split_requirements, redact_sensitive

def parse_jd_and_resumes(jd_text: str, candidates: list[dict]):
    jd_clean = normalize_text(jd_text)
    jd_items = split_requirements(jd_clean)

    cand_struct = []
    for c in candidates:
        raw = c["raw_text"]
        redacted = redact_sensitive(raw)
        cand_struct.append({
            "candidate_id": c["candidate_id"],
            "text": normalize_text(redacted)
        })

    jd_struct = {"raw": jd_clean, "items": jd_items}

    ev = TraceEvent(
        step="1",
        agent="ParserAgent",
        status="ok",
        summary=f"Parsed JD into {len(jd_items)} requirement items; normalized + redacted {len(cand_struct)} resumes.",
        details="\n".join(jd_items[:12])
    )
    return jd_struct, cand_struct, ev
