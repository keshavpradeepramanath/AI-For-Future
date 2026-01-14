import streamlit as st
import asyncio
from orchestrator import run_support_agent
from executors import execute_final_action

st.set_page_config(page_title="HITL Support Agent", layout="centered")

st.title("🧑‍⚖️ Human-in-the-Loop Support Agent")

ticket = st.text_area("Customer Ticket")

if "agent_state" not in st.session_state:
    st.session_state.agent_state = None

if st.button("Run Agent"):
    with st.spinner("Agent drafting response..."):
        st.session_state.agent_state = asyncio.run(
            run_support_agent(ticket)
        )

state = st.session_state.agent_state

if state:
    st.subheader("🧠 Agent Understanding")
    st.json(state["plan"])

    st.subheader("✍️ Draft Response")
    st.write(state["draft"]["draft_response"])
    st.write("Priority:", state["draft"]["priority"])

    if state["approval_required"]:
        st.warning("⚠️ Human approval required")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approve"):
                result = asyncio.run(
                    execute_final_action(state["draft"])
                )
                st.success(result)

        with col2:
            if st.button("❌ Reject"):
                st.error("Draft rejected. Manual handling required.")
    else:
        result = asyncio.run(execute_final_action(state["draft"]))
        st.success(result)
