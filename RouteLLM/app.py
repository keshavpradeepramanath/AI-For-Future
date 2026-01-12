import streamlit as st
from router.route_llm import route_query
from agents.critic_agent import critique
from llms.weak_llm import weak_llm_answer
from llms.strong_llm import strong_llm_answer


st.title("Agentic RouteLLM – Weak vs Strong LLM")

query = st.text_area("Ask your question")

def route_query(query: str):
    q = query.lower().strip()

    # HARD STOP — SIMPLE QUESTIONS
    if q.startswith(("what is", "define", "explain", "meaning of")):
        return "weak", 0.0, {"reason": "hardcoded_simple"}

    # STRONG MUST BE EXPLICIT
    strong_triggers = [
        "design", "architecture", "compare", "optimize",
        "scalable", "strategy", "tradeoff"
    ]

    if not any(t in q for t in strong_triggers):
        return "weak", 0.2, {"reason": "no_strong_trigger"}

    return "strong", 0.9, {"reason": "explicit_design_intent"}


if st.button("Submit") and query:
    route, score, signals = route_query(query)

    if route in ["weak", "weak+critic"]:
        answer = weak_llm_answer(query)
        verdict = critique(answer, query)

    if verdict == "ESCALATE":
        answer = strong_llm_answer(query)
        route = "strong (critic escalated)"


    st.markdown(f"### 🧠 Routed To: `{route}`")
    st.markdown(f"**Complexity Score:** `{score:.2f}`")
    st.json(signals)
    st.markdown("### ✅ Answer")
    st.write(answer)

    st.write(route_query("Define embeddings"))
    st.write(route_query("What is LLM"))

    st.write("TEST 1:", route_query("Define embeddings"))
    st.write("TEST 2:", route_query("What is LLM"))
    st.write("TEST 3:", route_query("Explain transformers"))
    st.write("TEST 4:", route_query("Design an embedding strategy"))


    st.subheader("🧪 Routing Explanation")
    st.write("Route:", route)
    st.write("Score:", score)
    st.json(signals)

