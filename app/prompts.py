RESTRUCTURE_PROMPT = """
You are an expert career coach and ATS resume optimizer.

Given the following resume and job description:

Resume:
{resume_text}

Job Description:
{job_description}

1. Rewrite and restructure the resume so it is highly relevant to the job description.
2. Maintain a professional tone and ATS-friendly formatting (no images, no tables).
3. Highlight key skills and experiences that match the JD.
4. Return ONLY the rewritten resume text.
"""

ATS_SCORE_PROMPT = """
You are an ATS scoring assistant.

Compare the following resume with the job description and give:
1. An ATS score from 0 to 100.
2. A short explanation for the score (e.g., missing keywords, structure issues, irrelevant content).

Resume:
{resume_text}

Job Description:
{job_description}
"""
