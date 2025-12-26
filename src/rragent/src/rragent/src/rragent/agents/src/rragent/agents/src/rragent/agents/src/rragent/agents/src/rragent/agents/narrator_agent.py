from rragent.schema import TraceEvent

def narrate(jd_struct: dict, scored: list[dict]):
    ranked = []
    for row in scored:
        top_hits = row.get("top_matches", [])[:5]
        narrative = (
            f"Overall score {row['score_total']:.1f}. "
            f"Strongest alignment: {', '.join(top_hits) if top_hits else 'general keyword overlap'}. "
            f"Evidence attached below. Human review required."
        )
        ranked.append({**row, "narrative": narrative})

    ev = TraceEvent(
        step="5",
        agent="NarratorAgent",
        status="ok",
        summary="Generated human-readable shortlist summaries (no auto-reject; evidence-first)."
    )
    return ranked, ev
