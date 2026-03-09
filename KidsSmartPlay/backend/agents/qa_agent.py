# backend/agents/qa_agent.py

from schemas.game_schema import Game


def qa_agent(state):

    try:

        if "answer" in state:
            state["answer"] = str(state["answer"])

        validated = Game(**state)

        return validated.dict()

    except Exception as e:

        return {
            "error": "QA validation failed",
            "details": str(e)
        }