import streamlit as st

st.title("Routing Test")

def weak_llm_answer(q):
    return "WEAK ANSWER"

def strong_llm_answer(query):
    return f"[STRONG LLM] Deep answer for: {query}"


def route_query(query: str):
    q = query.lower()
    print("DEBUG QUERY:", q)

    if "design" in q:
        print("DEBUG: DESIGN MATCHED")
        return "strong"

    print("DEBUG: FALLBACK WEAK")
    return "weak"

query = st.text_input("Ask")

if query:
    # 1️⃣ Routing (THIS defines meta – do not move this line)
    route = route_query(query)

    if route == "strong":
        answer = strong_llm_answer(query)
    else:
        answer = weak_llm_answer(query)

    st.markdown(f"### 🧠 Routed To: `{route}`")
    st.write(answer)

