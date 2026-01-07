import streamlit as st
import os
from orchestrator import orchestrate

st.set_page_config(page_title="Agentic AI Demo", layout="wide")

st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.sidebar.warning("Please enter your OpenAI API key")


st.title("🤖 Agentic AI with Orchestrator (Streamlit)")
st.write("A simple example of multi-agent collaboration")

query = st.text_input("Enter your question:")

if st.button("Run Agents"):
    if not query:
        st.warning("Please enter a query")
    else:
        with st.spinner("Agents are thinking..."):
            result = orchestrate(query)

            st.write("Research used:", result["used_research"])
            st.write("Planning used:", result["used_planning"])

            st.success(result["final"])


        st.subheader("🔍 Research Agent Output")
        st.write(result["used_research"])

        st.subheader("🧠 Planning Agent Output")
        st.write(result["used_planning"])

        st.subheader("✍️ Final Answer (Writer Agent)")
        st.success(result["final"])
