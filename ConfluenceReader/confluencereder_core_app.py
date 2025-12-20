"""
Streamlit + LangChain RAG App for Confluence
------------------------------------------
Features:
- Connects to Confluence using REST API
- Loads pages from selected spaces
- Chunks & embeds content
- Builds FAISS vector store
- Conversational Q&A with source citations

Run:
    streamlit run app.py
"""

import os
import streamlit as st
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Confluence RAG Assistant", layout="wide")
st.title("📘 Confluence Knowledge Assistant")

# -------------------------------
# Sidebar: OpenAI API Key
# -------------------------------
st.sidebar.subheader("🔑 OpenAI API Key")
openai_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
else:
    st.sidebar.warning("OpenAI API key required")

# -------------------------------
# Sidebar: Confluence Settings
# -------------------------------
st.sidebar.subheader("🔗 Confluence Connection")
conf_url = st.sidebar.text_input("Confluence Base URL", "https://yourcompany.atlassian.net/wiki")
conf_user = st.sidebar.text_input("Confluence Email")
conf_token = st.sidebar.text_input("Confluence API Token", type="password")
conf_space = st.sidebar.text_input("Space Key (e.g. ENG, OPS)")

load_btn = st.sidebar.button("Load Confluence Data")

# -------------------------------
# Session State
# -------------------------------
if "qa" not in st.session_state:
    st.session_state.qa = None
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Load + Index Confluence
# -------------------------------
if load_btn:
    if not all([conf_url, conf_user, conf_token, conf_space, openai_key]):
        st.error("Please fill all Confluence and OpenAI fields")
        st.stop()

    with st.spinner("Loading pages from Confluence..."):
        loader = ConfluenceLoader(
            url=conf_url,
            username=conf_user,
            api_key=conf_token,
            space_key=conf_space,
            include_attachments=False
        )
        print(f"Space is {conf_space} ")
        docs = loader.load()

    if not docs:
        st.error("No pages found in this space")
        st.stop()

    st.success(f"Loaded {len(docs)} pages. Chunking...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    st.info(f"Created {len(chunks)} chunks. Embedding...")

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    st.session_state.qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    st.session_state.history = []
    st.success("Confluence indexed. You can start asking questions.")

# -------------------------------
# Chat Interface
# -------------------------------
st.markdown("---")
st.subheader("💬 Ask Confluence")

query = st.text_input("Your question")

if st.button("Ask") and query:
    if not st.session_state.qa:
        st.warning("Load Confluence data first")
    else:
        result = st.session_state.qa({
            "question": query,
            "chat_history": st.session_state.history
        })

        answer = result.get("answer", "")
        sources = result.get("source_documents", [])

        st.session_state.history.append((query, answer))

        st.markdown("### ✅ Answer")
        st.write(answer)

        if sources:
            st.markdown("### 📚 Sources")
            for i, doc in enumerate(sources):
                meta = doc.metadata
                st.markdown(f"**{i+1}. {meta.get('title', 'Confluence Page')}**")
                st.markdown(meta.get("url", ""))

# -------------------------------
# Conversation History
# -------------------------------
st.markdown("---")
st.subheader("🕘 Chat History")
for q, a in st.session_state.history:
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")
    st.markdown("---")
