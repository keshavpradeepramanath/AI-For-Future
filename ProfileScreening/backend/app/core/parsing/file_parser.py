import PyPDF2
import docx


def parse_file(upload_file) -> str:
    filename = upload_file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(upload_file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif filename.endswith(".docx"):
        doc = docx.Document(upload_file.file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif filename.endswith(".txt"):
        return upload_file.file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
