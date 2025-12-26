import re
from rapidfuzz import fuzz

def normalize_text(t: str) -> str:
    t = t.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.lower().strip()

def split_requirements(jd: str) -> list[str]:
    # naive extraction: lines with bullets or requirement-like phrases
    lines = [x.strip("•-* \t") for x in jd.splitlines() if x.strip()]
    items = []
    for ln in lines:
        if len(ln) < 6:
            continue
        if any(k in ln for k in ["require", "must", "experience", "proficient", "skill", "responsib"]):
            items.append(ln)
        elif ln.startswith(("•", "-", "*")):
            items.append(ln)
    # fallback: take top lines if nothing matched
    return items[:40] if items else lines[:40]

def redact_sensitive(t: str) -> str:
    # remove email/phone (basic)
    t = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[email_redacted]", t)
    t = re.sub(r"\b(\+?\d[\d\-\(\) ]{8,}\d)\b", "[phone_redacted]", t)
    return t

def best_snippet(resume_text: str, jd_item: str, window: int = 260) -> str | None:
    # find best matching line for jd_item
    best = ("", 0)
    for line in resume_text.splitlines():
        s = fuzz.partial_ratio(jd_item[:120], line[:300])
        if s > best[1]:
            best = (line, s)
    if best[1] >= 75 and best[0].strip():
        return best[0].strip()[:window]
    return None
