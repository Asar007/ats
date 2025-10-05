from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.utils import extract_text_from_pdf, call_openai
from app.prompts import RESTRUCTURE_PROMPT, ATS_SCORE_PROMPT

app = FastAPI()

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile, job_description: str = Form(...)):
    # 1. Extract text from uploaded PDF
    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)

    # 2. Restructure resume
    restructure_prompt = RESTRUCTURE_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description
    )
    rewritten_resume = call_openai(restructure_prompt)

    # 3. Get ATS Score
    score_prompt = ATS_SCORE_PROMPT.format(
        resume_text=rewritten_resume,
        job_description=job_description
    )
    ats_score = call_openai(score_prompt)

    return {
        "rewritten_resume": rewritten_resume,
        "ats_score": ats_score
    }
