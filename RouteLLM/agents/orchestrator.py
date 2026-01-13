from router.intent_classifier import classify_intent
from router.model_router import route_model
from llms.mock_llm import mock_llm_call

def routing_agent(query: str):
    intent = classify_intent(query)
    model = route_model(intent)
    output = mock_llm_call(model)

    return {
        "intent": intent,
        "model": model,
        "output": output
    }
