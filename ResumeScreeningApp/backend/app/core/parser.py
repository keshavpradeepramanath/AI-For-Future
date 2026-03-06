from io import BytesIO
from fastapi import UploadFile
import docx
import PyPDF2


async def extract_text(file: UploadFile):

    content = await file.read()

    filename = file.filename.lower()

    # TEXT FILE
    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    # PDF FILE
    if filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(BytesIO(content))
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        return text

    # DOCX FILE
    if filename.endswith(".docx"):
        doc = docx.Document(BytesIO(content))
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    raise ValueError("Unsupported file format")
