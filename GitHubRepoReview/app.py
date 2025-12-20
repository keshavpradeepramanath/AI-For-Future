import os
import streamlit as st

st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.sidebar.warning("Please enter your OpenAI API key")

import streamlit as st
from reviewer import run_review

st.title("🧠 Autonomous GitHub Code Review Agent (MVP)")

repo_url = st.text_input("GitHub repo URL (public)", "https://github.com/owner/repo")

if st.button("Run Review"):
    try:
        owner, repo = repo_url.rstrip("/").split("/")[-2:]
        with st.spinner("Reviewing GitHub repository..."):
            results = run_review(owner, repo)

        for file, review in results.items():
            st.subheader(file)
            st.write(review)

    except Exception as e:
        st.error(f"Error: {e}")
