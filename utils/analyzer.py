import os
import re
import time
from openai import OpenAI

GROK_MODEL = "grok-4.3"
MAX_RETRIES = 3


def _call_grok(prompt: str, temperature: float = 0.3) -> str:
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        raise ValueError("GROK_API_KEY not set")

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=GROK_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            err_str = str(e)
            if "429" in err_str and attempt < MAX_RETRIES - 1:
                match = re.search(r"retry after (\d+)", err_str)
                delay = float(match.group(1)) + 1 if match else 2 ** attempt * 5
                time.sleep(delay)
                continue
            raise


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
    return _call_grok(prompt, temperature=0.1)


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
    return _call_grok(prompt, temperature=0.3)


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
    return _call_grok(prompt, temperature=0.5)
