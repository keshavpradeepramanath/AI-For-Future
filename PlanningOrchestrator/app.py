import streamlit as st
import os
from orchestrator import orchestrate

st.set_page_config(page_title="Agentic AI Demo", layout="wide")

st.sidebar.subheader("🔑 gemini API Key")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
else:
    st.sidebar.warning("Please enter your Gemini API key")


st.title("🤖 Agentic AI with Orchestrator (Streamlit)")
st.write("A simple example of multi-agent collaboration")

query = st.text_input("Enter your question:")

if st.button("Run Agents"):
    if not query:
        st.warning("Please enter a query")
    else:
        with st.spinner("Agents are thinking..."):
            result = orchestrate(query)

            st.write("🔁 Retried for quality:", result["retried"])

            st.write("Research used:", result["trace"])
            st.write("Planning used:", result["trace"])

            st.caption(f"🧠 Intent: {result['intent']}")
            st.caption(f"📊 Confidence: {result['confidence']}")
            st.caption(
                "🧩 Trace: " +
                " → ".join(f"{t['agent']} ({t['ms']}ms)" for t in result["trace"])
            )


            st.success(result["final"])


        st.subheader("🔍 Research Agent Output")
        st.write(result["trace"])

        st.subheader("🧠 Planning Agent Output")
        st.write(result["trace"])

        st.subheader("✍️ Final Answer (Writer Agent)")
        st.success(result["final"])
