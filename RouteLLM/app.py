import streamlit as st
from router.intent_classifier import classify_intent
from router.model_router import route_model 
from llms.mock_llm import mock_llm_call

st.title("Routing Test")

def weak_llm_answer(q):
    return "WEAK ANSWER"

def strong_llm_answer(query):
    return f"[STRONG LLM] Deep answer for: {query}"

def routing_agent(query: str):
    intent = classify_intent(query)
    model = route_model(intent)

    return {
        "intent": intent,
        "model": model,
        "output": mock_llm_call(model)
    }


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
    result = routing_agent(query)

    st.markdown(f"### 🧠 Routed Model: `{result['model']}`")
    st.write("Intent:", result["intent"])
    st.write("Output:", result["output"])

    # 1️⃣ Routing (THIS defines meta – do not move this line)
    route = route_query(query)

    if route == "strong":
        answer = strong_llm_answer(query)
    else:
        answer = weak_llm_answer(query)

    st.markdown(f"### 🧠 Routed To: `{route}`")
    st.write(answer)

