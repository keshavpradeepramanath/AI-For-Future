import streamlit as st

from config.settings import SETTINGS, SHAREPOINT
from core.llm_factory import LLMFactory
from core.rag_engine import RAGEngine
from retrieval.vector_store import InMemoryVectorStore
from retrieval.retriever import HybridRetriever
from ingestion.sharepoint_loader import SharePointLoader
from ingestion.ingestion_service import IngestionService
from ui.chat_ui import render_chat
from ui.voice_ui import render_voice

# --------------------------------------------------
# App metadata
# --------------------------------------------------
st.set_page_config(page_title=SETTINGS.APP_NAME)
st.title(SETTINGS.APP_NAME)

# --------------------------------------------------
# Display knowledge source (important for trust)
# --------------------------------------------------
st.caption(
    f"📂 Knowledge Source: {SHAREPOINT.SITE_URL}"
    f"{SHAREPOINT.ROOT_FOLDER}"
)

# --------------------------------------------------
# Dependency wiring (NO business logic)
# --------------------------------------------------
vector_store = InMemoryVectorStore()
retriever = HybridRetriever(vector_store)
llm = LLMFactory.create(SETTINGS.DEFAULT_LLM_PROVIDER)
rag_engine = RAGEngine(llm, retriever)

# --------------------------------------------------
# Controlled ingestion
# --------------------------------------------------
if SETTINGS.ENABLE_INGESTION_ON_STARTUP:
    loader = SharePointLoader(
        site_url=SHAREPOINT.SITE_URL,
        library=SHAREPOINT.DOCUMENT_LIBRARY,
        root_folder=SHAREPOINT.ROOT_FOLDER
    )

    ingestion_service = IngestionService(loader, vector_store)
    ingestion_service.ingest()

# --------------------------------------------------
# UI
# --------------------------------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🎙 Voice"])

with tab1:
    render_chat(rag_engine)

with tab2:
    if SETTINGS.VOICE_ENABLED:
        render_voice()
