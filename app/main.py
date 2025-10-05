import asyncio
import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks, Depends, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Assuming these are your utility functions and prompts
from app.utils import extract_text_from_pdf, call_openai
from app.prompts import RESTRUCTURE_PROMPT, ATS_SCORE_PROMPT, KEYWORD_ANALYSIS_PROMPT, RESTRUCTURE_LATEX_PROMPT
from app.latex_utils import latex_to_pdf


# --- Lifespan Management for Cleanup ---
# A more modern approach than on_startup/on_shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    # Example: Create a temporary directory for PDFs if it doesn't exist
    if not os.path.exists("temp_files"):
        os.makedirs("temp_files")
    yield
    # Code to run on shutdown
    # Example: Clean up any remaining files on shutdown
    for filename in os.listdir("temp_files"):
        os.remove(os.path.join("temp_files", filename))


app = FastAPI(lifespan=lifespan)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependency for Resume Processing ---
async def get_resume_text_from_pdf(file: UploadFile = Form(...)) -> str:
    """
    Dependency to read an uploaded PDF file, extract its text, and handle errors.
    This avoids code duplication in the endpoints.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    try:
        # file.read() is async, so it's non-blocking
        file_bytes = await file.read()
        # extract_text_from_pdf is a sync function, run it in a thread
        resume_text = await asyncio.to_thread(extract_text_from_pdf, file_bytes)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be empty or image-based.")
        return resume_text
    except Exception as e:
        # Catch-all for any other unexpected errors during file processing
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


# --- API Endpoints ---

# --- Combined Endpoint ---
@app.post("/optimize_resume")
async def optimize_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Accepts a resume PDF and job description, analyzes and rewrites the resume to maximize ATS score, and returns the rewritten resume and new ATS score.
    """
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    try:
        file_bytes = await resume_file.read()
        resume_text = await asyncio.to_thread(extract_text_from_pdf, file_bytes)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be empty or image-based.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    try:
        # Rewrite resume to maximize ATS score
        restructure_prompt = RESTRUCTURE_PROMPT.format(resume_text=resume_text, job_description=job_description)
        rewritten_resume = await asyncio.to_thread(call_openai, restructure_prompt)

        # Get new ATS score for rewritten resume
        score_prompt = ATS_SCORE_PROMPT.format(resume_text=rewritten_resume, job_description=job_description)
        new_ats_score = await asyncio.to_thread(call_openai, score_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while communicating with the AI model: {e}")

    return {
        "rewritten_resume": rewritten_resume,
        "new_ats_score": new_ats_score.strip()
    }


@app.post("/generate_pdf")
async def generate_resume_pdf(
    background_tasks: BackgroundTasks,
    job_description: str = Form(...),
    resume_text: str = Depends(get_resume_text_from_pdf)
):
    """
    Generates an optimized resume in PDF format from a resume and job description.
    """
    try:
        # --- Generate LaTeX content ---
        restructure_prompt = RESTRUCTURE_LATEX_PROMPT.format(resume_text=resume_text, job_description=job_description)
        latex_resume = await asyncio.to_thread(call_openai, restructure_prompt)

        # --- Compile LaTeX to PDF (blocking call) ---
        pdf_path = await asyncio.to_thread(latex_to_pdf, latex_resume, "temp_files")
        if not pdf_path:
            raise HTTPException(status_code=500, detail="Failed to compile LaTeX to PDF.")

        # Add a background task to delete the file after sending it
        background_tasks.add_task(os.remove, pdf_path)

        return FileResponse(
            path=pdf_path,
            filename="optimized_resume.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during PDF generation: {e}")

