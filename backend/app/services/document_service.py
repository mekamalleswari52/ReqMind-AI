import os
from .extraction_service import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def extract_text(path: str, filename: str) -> str:
    lower = filename.lower()
    if lower.endswith('.pdf'):
        return extract_text_from_pdf(path)
    if lower.endswith('.docx'):
        return extract_text_from_docx(path)
    if lower.endswith('.txt'):
        return extract_text_from_txt(path)
    return ""
