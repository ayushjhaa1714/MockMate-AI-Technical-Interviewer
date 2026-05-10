# backend/app/utils/pdf_parser.py
import io
from fastapi import UploadFile
from pypdf import PdfReader

async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Reads a PDF file upload and returns plain text.
    """
    # Read the file into memory
    content = await file.read()
    
    # Create a PDF object
    pdf_stream = io.BytesIO(content)
    reader = PdfReader(pdf_stream)
    
    text = ""
    # Loop through each page and extract text
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    return text.strip()