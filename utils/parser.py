import io
import PyPDF2

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = []
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)
