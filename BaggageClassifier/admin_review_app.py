import streamlit as st
from rule_extractor import extract_rules
from db import save_rule

st.title("🔐 Airline Rule Review (Admin)")

policy_text = st.text_area("Paste Airline / IATA Policy Text")

if st.button("Extract Rules"):
    rules = extract_rules(policy_text)
    st.session_state.rules = rules

if "rules" in st.session_state:
    for rule in st.session_state.rules:
        st.subheader(f"Item: {rule['item']}")

        decision = st.selectbox(
            "Decision",
            ["cabin_allowed", "checkin_only", "not_allowed", "uncertain"],
            index=["cabin_allowed", "checkin_only", "not_allowed", "uncertain"]
            .index(rule["decision"])
        )

        reference = st.text_input("Reference", rule["reference"])

        if st.button(f"Approve {rule['item']}"):
            save_rule(
                authority="IATA",
                item=rule["item"],
                decision=decision,
                reference=reference
            )
            st.success("Rule saved")
