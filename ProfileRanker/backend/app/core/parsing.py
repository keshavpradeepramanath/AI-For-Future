import PyPDF2
import docx

def extract_text_from_file(upload_file):
    filename = upload_file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(upload_file.file)
        return "".join([p.extract_text() or "" for p in reader.pages])

    elif filename.endswith(".docx"):
        doc = docx.Document(upload_file.file)
        return "\n".join([p.text for p in doc.paragraphs])

    elif filename.endswith(".txt"):
        return upload_file.file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type")
