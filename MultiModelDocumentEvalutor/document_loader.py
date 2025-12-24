from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile

def load_document(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    if uploaded_file.name.endswith(".pdf"):
        docs = PyPDFLoader(path).load()
    else:
        docs = TextLoader(path).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    return "\n".join([c.page_content for c in chunks])
