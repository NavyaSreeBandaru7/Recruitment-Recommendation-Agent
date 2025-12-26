import re
from rapidfuzz import fuzz

SKILL_WORDS = [
    "python","sql","power bi","tableau","excel","aws","gcp","azure",
    "etl","dashboard","machine learning","nlp","statistics","ab testing",
    "hris","adp","ukg","workday","compensation","pay equity"
]

def _count_hits(text: str, phrases: list[str]) -> tuple[int, list[str]]:
    hits = []
    for p in phrases:
        if p in text:
            hits.append(p)
    return len(hits), hits

def _experience_signal(text: str) -> float:
    # naive: count occurrences like "3 years", "5+ years"
    matches = re.findall(r"(\d+)\s*\+?\s*years", text)
    if not matches:
        return 0.0
    years = max(int(x) for x in matches)
    return min(years / 10.0, 1.0)  # cap at 10 years

def score_candidate(jd_items: list[str], resume_text: str, weights: dict) -> dict:
    # Skills score
    skill_hits, hit_list = _count_hits(resume_text, SKILL_WORDS)
    score_skill = min(skill_hits / 12.0, 1.0) * weights["skill"]

    # Responsibilities match (fuzzy against JD requirement lines)
    resp_scores = []
    top_matches = []
    for item in jd_items[:20]:
        s = fuzz.partial_ratio(item[:160], resume_text[:5000]) / 100.0
        resp_scores.append(s)
    resp = (sum(resp_scores) / max(len(resp_scores), 1)) if resp_scores else 0.0
    score_resp = resp * weights["resp"]

    # Experience signal
    exp = _experience_signal(resume_text)
    score_exp = exp * weights["exp"]

    # Other keyword overlap (very light)
    other = (0.2 if "project" in resume_text and "project" in " ".join(jd_items) else 0.0)
    score_other = other * weights["other"]

    total = score_skill + score_resp + score_exp + score_other

    # add some interpretable top items
    top_matches = hit_list[:8]

    return {
        "score_skill": round(score_skill, 2),
        "score_resp": round(score_resp, 2),
        "score_exp": round(score_exp, 2),
        "score_other": round(score_other, 2),
        "score_total": round(total, 2),
        "top_matches": top_matches
    }
