# Recruitment Recommendation Agent (Multi-Agent) — Streamlit + Hugging Face Spaces

Link: https://huggingface.co/spaces/Navya-Sree/Recruitment-Recommendation-Agent

A multi-agent **HR shortlisting assistant** that ranks candidates for a job opening using an “HR committee” workflow:

**Parser → Matcher → Evidence → Fairness/Compliance → Narrator**

It produces:
- ✅ Ranked shortlist with interpretable scores  
- ✅ Evidence snippets (where each match came from in the resume)  
- ✅ Fairness/compliance flags (protected/sensitive attribute hints)  
- ✅ A trace timeline showing what each agent did (transparency / trust)

> **Important:** This tool is for **decision support**. It must not be used for automated hiring decisions. Always keep a human in the loop.

---

## Demo Workflow

1. Paste a **Job Description (JD)**  
2. Upload multiple candidate **resumes as `.txt`**  
3. Click **Run Shortlisting**  
4. Review:
   - shortlist ranking table  
   - candidate narrative summary  
   - evidence snippets  
   - fairness/compliance flags  
   - trace timeline  

---

## Why this project stands out

Most “resume matchers” are keyword search. This project is different because it:
- Uses **multiple specialized agents** (like a real hiring committee)
- Is **evidence-first** (every match shows supporting resume text)
- Includes **fairness/compliance guardrails** (flags sensitive/protected hints)
- Provides a **trace timeline** for transparency (“what the AI did”)

---

## Architecture

### Agents
- **ParserAgent**: Cleans text, extracts JD requirement items, redacts basic PII (email/phone).
- **MatcherAgent**: Scores candidates with weighted matching (skills, responsibilities, experience, other).
- **EvidenceAgent**: Extracts best resume snippets supporting top JD items.
- **FairnessAgent**: Flags protected/sensitive attribute hints (do-not-use signals).
- **NarratorAgent**: Writes a human-readable summary per candidate.

### Orchestrator
`run_pipeline()` runs agents in order and collects:
- ranked candidates
- evidence snippets
- flags
- trace events

---

## Tech Stack
- **Streamlit** (UI)
- **Python**
- **rapidfuzz** (fuzzy matching)
- **pandas / numpy / scikit-learn** (scoring utilities)

---

## Project Structure

