from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import asyncio
import re

from agents.jd_agent import parse_jd
from agents.screening_agent import screen_candidate_multi
from agents.ranking_agent import rank_candidates

from utils.file_parser import read_file

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔹 Helpers
# =========================

def extract_score(text):
    match = re.search(r"Score:\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def extract_matched_jd(text):
    match = re.search(r"Matched JD:\s*(.*)", text)
    return match.group(1).strip() if match else "Unknown JD"

def extract_decision(text):
    match = re.search(r"Decision:\s*(SELECT|REJECT)", text)
    return match.group(1) if match else "REJECT"


def extract_reason(text):
    match = re.search(r"Reasoning:\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else text


def extract_summary(text):
    match = re.search(r"Summary:\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_name(resume_text):
    lines = resume_text.split("\n")

    for line in lines[:10]:
        line = line.strip()

        if "@" in line or any(char.isdigit() for char in line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4 and len(line) < 40:
            return line.title()

    return "Unknown Candidate"


# =========================
# 🔹 Multi-JD Resume Processing
# =========================

from agents.screening_agent import screen_candidate_multi


async def process_resume_multi(resume_file, parsed_jds):
    try:
        resume_text = read_file(resume_file)

        if not resume_text:
            raise Exception("Empty resume")

        resume_text = resume_text[:12000]

        name = extract_name(resume_text)

        # ✅ SINGLE LLM CALL
        output = screen_candidate_multi(parsed_jds, resume_text)

        matched_jd = extract_matched_jd(output)
        score = extract_score(output)
        decision = extract_decision(output)
        reason = extract_reason(output)
        summary = extract_summary(output)

        return {
            "resume": name,
            "matched_jd": matched_jd,
            "score": score,
            "decision": decision,
            "reason": reason,
            "summary": summary
        }

    except Exception as e:
        return {
            "resume": resume_file.filename,
            "matched_jd": "N/A",
            "score": 0,
            "decision": "REJECT",
            "reason": str(e),
            "summary": ""
        }

# =========================
# 🔹 API
# =========================

@app.post("/screen")
async def screen_resumes(
    jds: list[UploadFile] = File(...),
    resumes: list[UploadFile] = File(...)
):
    parsed_jds = []

    # ✅ Parse all JDs
    for jd_file in jds:
        jd_text = read_file(jd_file)[:15000]
        parsed = parse_jd(jd_text)

        parsed_jds.append({
            "name": jd_file.filename,
            "content": parsed
        })

    # ✅ Parallel resume processing
    tasks = [process_resume_multi(r, parsed_jds) for r in resumes]
    results = await asyncio.gather(*tasks)

    # ✅ Ranking
    ranked = rank_candidates(results)

    return {"ranked_candidates": ranked}


@app.get("/")
def health():
    return {"status": "ok"}
