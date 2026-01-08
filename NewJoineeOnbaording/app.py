import streamlit as st
from orchestrator import orchestrate_onboarding

st.set_page_config(
    page_title="New Comer Onboarding",
    layout="wide"
)


if "onboarded_members" not in st.session_state:
    st.session_state.onboarded_members = []


st.title("👋 New Comer Onboarding Portal")

with st.form("onboarding_form"):
    name = st.text_input("Full Name")
    role = st.text_input("Role")
    department = st.selectbox(
        "Department",
        ["Engineering", "Product", "HR", "Sales"]
    )

    submitted = st.form_submit_button("Start Onboarding")

if submitted:
    # ✅ DEFINE profile HERE
    profile = {
        "name": name,
        "role": role,
        "department": department
    }

    with st.spinner("Setting things up..."):
        result = orchestrate_onboarding(profile)

    st.success("🎉 Onboarding Completed!")

    # ✅ BUILD member record HERE (profile exists)
    member_record = {
        "name": profile["name"],
        "employee_id": result["profile"]["employee_id"],
        "status": {
            "Profile Created": "✅",
            "Email Assigned": "✅" if result["it_access"]["email_access"] else "❌",
            "WiFi Access": "✅" if result["it_access"]["wifi_access"] else "❌",
            "Software Access": "✅",
            "Buddy Assigned": "✅",
            "Docs Shared": "✅"
        }
    }

    # ✅ STORE in session state
    st.session_state.onboarded_members.append(member_record)

    with st.spinner("Setting things up..."):
        result = orchestrate_onboarding(profile)

    st.success("🎉 Onboarding Completed!")

    st.subheader("🧠 Agent Execution Trace")
    st.write(" → ".join(result["trace"]))

    st.subheader("👤 Profile")
    st.json(result["profile"])

    st.subheader("💻 IT Access")
    st.json(result["it_access"])

    st.subheader("🤝 Buddy Assigned")
    st.info(result["buddy"])

    st.subheader("📚 Knowledge & Docs")
    st.json(result["knowledge"])

    st.divider()
    st.header("📋 Onboarded Members & Status")

    if not st.session_state.onboarded_members:
        st.info("No members onboarded yet.")
    else:
        for member in st.session_state.onboarded_members:
            with st.expander(f"👤 {member['name']} ({member['employee_id']})"):
                for topic, status in member["status"].items():
                    st.write(f"{status} {topic}")

