import os
import glob
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# st.set_page_config(page_title="Simple Document Chat", layout="wide")
st.title("📄 Simple Conversational Document Chat (LangChain)")

# -------------------------------
# API Key Input
# -------------------------------
st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.sidebar.warning("Please enter your OpenAI API key to continue.")

# -------------------------------
# Helpers
# -------------------------------
def load_all_documents(folder):
    files = []
    for ext in ["*.pdf", "*.txt"]:
        files.extend(glob.glob(os.path.join(folder, ext)))

    docs = []
    for f in files:
        try:
            if f.endswith(".pdf"):
                docs.extend(PyPDFLoader(f).load())
            elif f.endswith(".txt"):
                docs.extend(TextLoader(f).load())
        except Exception as e:
            st.warning(f"Could not read {f}: {e}")
    return docs

# -------------------------------
# Session State
# -------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa" not in st.session_state:
    st.session_state.qa = None
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Sidebar
# -------------------------------
folder = st.sidebar.text_input("Folder path containing documents")
ingest_btn = st.sidebar.button("Load & Index Documents")

model_name = st.sidebar.selectbox("LLM", ["gpt-4o", "gpt-4o-mini"], index=1)
embed_model = st.sidebar.selectbox("Embeddings", ["text-embedding-ada-002"], index=0)

# -------------------------------
# Ingest & Chunk
# -------------------------------
if ingest_btn:
    if not folder or not os.path.exists(folder):
        st.error("Invalid folder path")
    else:
        st.info("Loading documents...")
        docs = load_all_documents(folder)

        if not docs:
            st.error("No documents found.")
        else:
            st.success(f"Loaded {len(docs)} documents. Building embeddings...")

            embeddings = OpenAIEmbeddings(model=embed_model)

            # Create chunker
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100
            )

            chunked_docs = splitter.split_documents(docs)

            # Original text+metadata arrays (no cleaning)
            texts = []
            metas = []

            for d in chunked_docs:
                text = d.page_content.strip() if hasattr(d, "page_content") else ""
                if len(text) > 5:
                    texts.append(text)
                    metas.append(d.metadata if hasattr(d, "metadata") else {})

            st.write("Chunks:", len(texts), "Metadata:", len(metas))

            min_len = min(len(texts), len(metas))
            texts = texts[:min_len]
            metas = metas[:min_len]

            # Original FAISS build
            # vs = FAISS.from_texts(texts, embeddings, metadatas=metas)
            from langchain.schema import Document

            docs_for_faiss = []
            for i in range(len(texts)):
                docs_for_faiss.append(Document(
                    page_content=texts[i],
                    metadata=metas[i]
                ))

# vs = FAISS.from_documents(docs_for_faiss, embeddings)

            vs = FAISS.from_documents(docs_for_faiss, embeddings)
            st.session_state.vectorstore = vs

            llm = ChatOpenAI(model_name=model_name, temperature=0)
            retriever = vs.as_retriever(search_kwargs={"k": 4})

            st.session_state.qa = ConversationalRetrievalChain.from_llm(llm, retriever)

            st.success("Ready! Start chatting below.")

# -------------------------------
# Chat UI
# -------------------------------
st.subheader("Ask Questions About Your Documents")
user_q = st.text_input("Your question")

if st.button("Send") and user_q:
    if not st.session_state.qa:
        st.warning("Please load documents first.")
    else:
        result = st.session_state.qa({
            "question": user_q,
            "chat_history": st.session_state.history
        })

        answer = result.get("answer", "")
        st.session_state.history.append((user_q, answer))

        st.write(f"**You:** {user_q}")
        st.write(f"**Bot:** {answer}")

# -------------------------------
# Conversation history
# -------------------------------
st.markdown("---")
st.subheader("Conversation History")

for q, a in st.session_state.history:
    st.write(f"❓ **{q}**")
    st.write(f"💬 {a}")
    st.write("---")
