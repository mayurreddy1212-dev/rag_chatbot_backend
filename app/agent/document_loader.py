from pypdf import PdfReader
from docx import Document

def load_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_docx(file_path: str):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_txt(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
