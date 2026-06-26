import os
import streamlit as st
from dotenv import load_dotenv

from utils.parser import extract_text_from_pdf
from utils.analyzer import parse_resume, analyze_match, generate_cover_letter

load_dotenv()

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Smart Resume Analyzer")
st.markdown("Upload a resume, paste a job description, and get an AI-powered fit analysis.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📎 Upload Resume")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    resume_text = ""
    if resume_file:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(resume_file.read())
        if resume_text.strip():
            st.success(f"Extracted {len(resume_text)} characters from resume.")
            with st.expander("Preview extracted text"):
                st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
        else:
            st.error("Could not extract text. Try a different PDF.")

with col2:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste job description...",
    )

if not os.getenv("GOOGLE_API_KEY"):
    st.sidebar.warning("⚠️ GOOGLE_API_KEY not found. Set it in `.env` or as a Streamlit secret.")
st.sidebar.markdown("[Get a free Gemini API key](https://aistudio.google.com/app/apikey)")

st.sidebar.markdown("---")
st.sidebar.markdown("### How it works")
st.sidebar.markdown(
    """
1. Upload your resume (PDF)
2. Paste a job description
3. Click **Analyze**
4. Get match score, gaps, suggestions, and a cover letter
"""
)

if st.button("🔍 Analyze Match", type="primary", disabled=not (resume_text.strip() and job_description.strip())):
    if not resume_text.strip():
        st.error("Please upload a valid resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Match Analysis", "📝 Parsed Resume", "✉️ Cover Letter", "ℹ️ Raw Data"])

        with tab1:
            with st.spinner("Analyzing resume against job description..."):
                try:
                    result = analyze_match(resume_text, job_description)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

        with tab2:
            with st.spinner("Parsing resume structure..."):
                try:
                    parsed = parse_resume(resume_text)
                    st.markdown(parsed)
                except Exception as e:
                    st.error(f"Parsing failed: {e}")

        with tab3:
            name = ""
            with st.spinner("Generating cover letter..."):
                try:
                    parsed_raw = parse_resume(resume_text)
                    for line in parsed_raw.split("\n"):
                        if "name" in line.lower() and ":" in line:
                            name = line.split(":", 1)[1].strip().strip('"').strip(",")
                            break
                    cover = generate_cover_letter(resume_text, job_description, name or "Applicant")
                    st.markdown(cover)
                    st.download_button("Download Cover Letter", cover, file_name="cover_letter.txt")
                except Exception as e:
                    st.error(f"Cover letter generation failed: {e}")

        with tab4:
            st.subheader("Resume Text")
            st.text(resume_text)
            st.subheader("Job Description")
            st.text(job_description)

else:
    st.info("Upload a resume and paste a job description to get started.")
