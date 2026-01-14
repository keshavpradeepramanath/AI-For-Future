import streamlit as st
import asyncio
from orchestrator import run_support_agent

st.set_page_config(page_title="Support Ticket Agent", layout="centered")

st.title("🎧 Agentic Customer Support App")

ticket = st.text_area("Enter customer support ticket:")

if st.button("Process Ticket"):
    if ticket:
        with st.spinner("Agent processing ticket..."):
            output = asyncio.run(run_support_agent(ticket))

        st.subheader("🧠 Ticket Understanding")
        st.json(output["plan"])

        st.subheader("🤖 Routed Agent")
        st.write(output["agent_type"])

        st.subheader("⚙️ Agent Actions (Async)")
        st.json(output["results"])
    else:
        st.warning("Please enter a ticket.")
