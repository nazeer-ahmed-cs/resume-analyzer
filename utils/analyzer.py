import os
from google import genai

GEMINI_MODEL = "gemini-2.0-flash-lite"


def _call_gemini(prompt: str, temperature: float = 0.3) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"temperature": temperature},
    )
    return response.text


def parse_resume(resume_text: str) -> str:
    prompt = f"""Extract the following from this resume in a structured format:

Resume:
{resume_text}

Return a JSON-like structure with these fields:
- name: full name
- email: email address
- phone: phone number
- skills: list of technical skills
- experience: list of past roles (title, company, years)
- education: list of degrees
- projects: list of notable projects

Only include information present in the resume. If a field is missing, use null."""
    return _call_gemini(prompt, temperature=0.1)


def analyze_match(resume_text: str, job_description: str) -> str:
    prompt = f"""You are an expert technical recruiter. Analyze how well the following resume matches the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide a detailed analysis with:
1. **Match Score** (0-100): Overall percentage match
2. **Matched Skills**: Skills from the resume that match the job requirements
3. **Missing Skills**: Important skills mentioned in the job but absent from the resume
4. **Experience Fit**: How well the candidate's experience aligns with the role
5. **Education Fit**: Whether the education background matches requirements
6. **Key Strengths**: Top 3 reasons this candidate stands out
7. **Weaknesses**: Gaps or concerns
8. **Improvement Suggestions**: 3-5 actionable suggestions to make the resume stronger for this role"""
    return _call_gemini(prompt, temperature=0.3)


def generate_cover_letter(resume_text: str, job_description: str, name: str) -> str:
    prompt = f"""Write a professional cover letter for {name} applying to the role described below.

Resume Background:
{resume_text}

Job Description:
{job_description}

Write a concise, impactful cover letter (3-4 paragraphs) that:
1. Opens with enthusiasm for the role and company
2. Highlights 2-3 relevant achievements from the resume
3. Connects the candidate's skills to the job requirements
4. Closes with a call to action

Use a professional tone. Keep it under 300 words."""
    return _call_gemini(prompt, temperature=0.5)
