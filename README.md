# Smart Resume Analyzer

An AI-powered resume analyzer built with **Streamlit** and **Google Gemini**. Upload a resume, paste a job description, and get a detailed match analysis with improvement suggestions and a cover letter.

## Features

- **PDF Resume Parsing** — Extract text from uploaded PDF resumes
- **Match Analysis** — Compare resume against job description with a score out of 100
- **Skill Gap Detection** — Identify missing skills and keywords
- **Improvement Suggestions** — Actionable tips to optimize your resume
- **Cover Letter Generation** — AI-written cover letter tailored to the role
- **Structured Resume View** — Parse resume into clean sections

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.0 Flash Lite (free tier)
- **API SDK**: Google GenAI Python SDK
- **PDF Processing**: PyPDF2
- **Deployment**: Streamlit Cloud

## Getting Started

### Prerequisites

- Python 3.10+
- [Google Gemini API key](https://aistudio.google.com/app/apikey) (free)

### Installation

```bash
git clone https://github.com/nazeer-ahmed-cs/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your Gemini API key:
# GOOGLE_API_KEY=your_key_here
```

### Run Locally

```bash
streamlit run app.py
```

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Add `GOOGLE_API_KEY` as a Streamlit secret
5. Deploy

## Project Structure

```
resume-analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # API key template
├── utils/
│   ├── __init__.py
│   ├── parser.py       # PDF text extraction
│   └── analyzer.py     # LangChain + Gemini analysis chains
└── README.md
```

## What I Learned

- Building LLM-powered applications with Google Gemini API
- Structured text generation and prompt engineering
- PDF text extraction and preprocessing
- Prompt engineering for consistent structured output
- Deploying AI apps with Streamlit Cloud
