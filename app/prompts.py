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
KEYWORD_ANALYSIS_PROMPT = """
You are an ATS analysis assistant.

Compare the following resume and job description. Identify the top 15 keywords and phrases from the job description that are most relevant to the role.

Return a JSON object with two arrays:
- "matched_keywords": Keywords present in the resume.
- "missing_keywords": Keywords that are in the job description but not found in the resume.

Only return valid JSON, no explanations.

Resume:
{resume_text}

Job Description:
{job_description}
"""

RESTRUCTURE_LATEX_PROMPT = """
You are an expert resume writer and LaTeX document designer.

Your goal:
Rewrite the given resume to align strongly with the provided job description, while keeping the formatting identical to the example resume layout below.

Output must be in **LaTeX format**, fully compilable with `pdflatex`.

---

### TEMPLATE FORMAT (Do not modify structure, only replace content):

\\documentclass[a4paper,10pt]{article}
\\usepackage[margin=0.7in]{geometry}
\\usepackage[hidelinks]{hyperref}
\\usepackage{enumitem}
\\setlength{\\parindent}{0pt}
\\begin{document}

% === HEADER ===
\\textbf{\\LARGE {NAME}} \\\\
EMAIL | PHONE | LOCATION \\\\
\\href{LINKEDIN_URL}{LinkedIn} | \\href{GITHUB_URL}{GitHub} \\\\

% === EDUCATION ===
\\section*{EDUCATION}
\\textbf{Institution Name}, City, State \\\\
Degree, Major \\hfill Start – End Year \\\\
CGPA: X.XX/10.0 \\\\

% === EXPERIENCE ===
\\section*{EXPERIENCE}
\\textbf{Company Name} \\hfill Month Year \\\\
Position/Internship \\\\
\\begin{itemize}[noitemsep, topsep=0pt]
    \\item Bullet 1 describing achievement or contribution.
    \\item Bullet 2 describing measurable impact.
\\end{itemize}

% === PROJECTS ===
\\section*{PROJECTS}
\\textbf{Project Name} – Tools/Tech Used \\\\
\\begin{itemize}[noitemsep, topsep=0pt]
    \\item Bullet points describing the problem, solution, and results.
\\end{itemize}

% === TECHNICAL SKILLS ===
\\section*{TECHNICAL SKILLS}
Languages: ... \\\\
Frameworks: ... \\\\
Tools: ... \\\\
Others: ... \\\\

% === ACHIEVEMENTS & CERTIFICATIONS ===
\\section*{ACHIEVEMENTS \\& CERTIFICATIONS}
\\begin{itemize}[noitemsep, topsep=0pt]
    \\item Achievement or certification 1
    \\item Achievement or certification 2
\\end{itemize}

\\end{document}

---

### RULES:
1. Maintain **the same order of sections** and structure as shown.
2. Replace placeholders with rewritten content from the provided resume.
3. Emphasize alignment with the given Job Description.
4. Use concise, action-based bullet points (starting with action verbs).
5. Include quantifiable achievements and relevant keywords.
6. Preserve a clean, ATS-friendly single-column layout.
7 Rewrite all bullet points in the "Professional Experience" section to be achievement-focused.
    7.1 Prioritize the XYZ Formula: Structure accomplishments using the formula: "Accomplished [X] as measured by [Y] by doing [Z].
    7.2 Flexibility: If a specific metric (Y) is not available, rephrase the point to focus on the action and its positive business impact. Do not invent metrics.
7. Return **only valid LaTeX code**, no comments, no explanations.

---
RESUME CONTENT:
{resume_text}

---
JOB DESCRIPTION:
{job_description}
"""


