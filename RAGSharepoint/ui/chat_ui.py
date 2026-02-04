import streamlit as st

def render_chat(rag_engine):
    st.header("💬 Knowledge Chat")

    query = st.text_input("Ask a question")

    if st.button("Ask") and query:
        result = rag_engine.answer(query)

        st.write("### Answer")
        st.write(result["answer"])

        if result["sources"]:
            st.write("### Sources")
            for s in result["sources"]:
                st.write(f"- {s}")
