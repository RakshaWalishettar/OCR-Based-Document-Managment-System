# app/ocr.py
import tempfile
import subprocess
from typing import Optional
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_image_file(path: str) -> str:
    """
    Use pytesseract to extract text from image file.
    """
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf_file(path: str) -> str:
    """
    Convert PDF pages to images then run OCR.
    """
    pages = convert_from_path(path, dpi=200)
    text_parts = []
    for page in pages:
        text_parts.append(pytesseract.image_to_string(page))
    return "\n".join(text_parts)

def extract_text_generic(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext in [".pdf"]:
        return extract_text_from_pdf_file(path)
    # assume image
    return extract_text_from_image_file(path)
