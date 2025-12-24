import streamlit as st
import os
from document_loader import load_document
from agents.gpt_agent import run_gpt
from agents.gemini_agent import run_gemini,get_supported_gemini_models
#from agents.bedrock_agent import run_bedrock
from agents.judge_agent import judge_answers

st.set_page_config(page_title="Multi-Model Document QnA")
st.title("📊 Multi-Model Document Extraction & Evaluation")

# API keys
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key

gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
if gemini_key:
    os.environ["GOOGLE_API_KEY"] = gemini_key    

get_supported_gemini_models()

if "gemini_models" not in st.session_state:
    try:
        st.session_state.gemini_models = get_supported_gemini_models()
    except Exception as e:
        st.session_state.gemini_models = []
        st.warning(f"Could not fetch Gemini models: {e}")    

uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt"])
question = st.text_input("Ask a question from the document")

if uploaded_file and question and st.button("Run Extraction"):
    with st.spinner("Processing document..."):
        context = load_document(uploaded_file)

    st.info("Running models in parallel...")

    answers = {
        "GPT-3.5-turbo": run_gpt(context, question),
        "gemini-3-pro-preview": run_gemini(context, question)
    }

    st.subheader("📄 Model Answers")
    for model, ans in answers.items():
        st.markdown(f"### {model}")
        st.write(ans)

    st.subheader("⚖️ Judge Evaluation")
    verdict = judge_answers(question, answers)
    st.write(verdict)
