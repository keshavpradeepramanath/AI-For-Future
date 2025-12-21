import os
import streamlit as st
from agent import refine_prompt

st.title("🧠 Prompt Refinement Agent")

st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

user_prompt = st.text_area(
    "Enter your basic or vague prompt",
    placeholder="e.g. build an AI agent for code review"
)

if st.button("Refine Prompt") and user_prompt:
    with st.spinner("Refining prompt..."):
        refined = refine_prompt(user_prompt)

    st.subheader("✨ Improved Prompt")
    st.text_area("", refined, height=300)
