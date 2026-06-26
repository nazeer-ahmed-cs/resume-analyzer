import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

GEMINI_MODEL = "models/gemini-2.0-flash-lite"


def _get_llm(temperature: float = 0.3):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set")
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=api_key, temperature=temperature)


_STRUCTURE_PROMPT = PromptTemplate(
    input_variables=["resume_text"],
    template="""Extract the following from this resume in a structured format:

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

Only include information present in the resume. If a field is missing, use null.
""",
)

_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template="""You are an expert technical recruiter. Analyze how well the following resume matches the job description.

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
8. **Improvement Suggestions**: 3-5 actionable suggestions to make the resume stronger for this role
""",
)

_COVER_LETTER_PROMPT = PromptTemplate(
    input_variables=["resume_text", "job_description", "name"],
    template="""Write a professional cover letter for {name} applying to the role described below.

Resume Background:
{resume_text}

Job Description:
{job_description}

Write a concise, impactful cover letter (3-4 paragraphs) that:
1. Opens with enthusiasm for the role and company
2. Highlights 2-3 relevant achievements from the resume
3. Connects the candidate's skills to the job requirements
4. Closes with a call to action

Use a professional tone. Keep it under 300 words.
""",
)


def parse_resume(resume_text: str) -> str:
    llm = _get_llm(temperature=0.1)
    chain = LLMChain(llm=llm, prompt=_STRUCTURE_PROMPT)
    return chain.run(resume_text=resume_text)


def analyze_match(resume_text: str, job_description: str) -> str:
    llm = _get_llm(temperature=0.3)
    chain = LLMChain(llm=llm, prompt=_ANALYSIS_PROMPT)
    return chain.run(resume_text=resume_text, job_description=job_description)


def generate_cover_letter(resume_text: str, job_description: str, name: str) -> str:
    llm = _get_llm(temperature=0.5)
    chain = LLMChain(llm=llm, prompt=_COVER_LETTER_PROMPT)
    return chain.run(resume_text=resume_text, job_description=job_description, name=name)
