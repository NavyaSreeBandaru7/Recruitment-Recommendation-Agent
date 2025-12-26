from rragent.schema import TraceEvent

PROTECTED_HINTS = [
    "age", "years old", "date of birth", "dob",
    "gender", "female", "male", "married", "single",
    "religion", "church", "muslim", "hindu", "christian",
    "race", "ethnicity", "nationality",
    "disability", "disabled", "wheelchair",
    "pregnant", "pregnancy",
]

def fairness_check(scored: list[dict]):
    for c in scored:
        flags = []
        text = c["text"]
        for term in PROTECTED_HINTS:
            if term in text:
                flags.append(f"Sensitive attribute hint detected: '{term}'. Ensure it is NOT used for decisions.")
        c["flags"] = flags
        c["flags_count"] = len(flags)

    ev = TraceEvent(
        step="4",
        agent="FairnessAgent",
        status="ok",
        summary="Scanned resumes for protected/sensitive attribute hints and added compliance warnings (do-not-use signals)."
    )
    return scored, ev
