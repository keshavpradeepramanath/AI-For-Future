from openai import OpenAI
from prompts import ANSWER_PROMPT, CRITIQUE_PROMPT

def ask_llm(model, question):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=ANSWER_PROMPT.format(question=question)
    )
    return response.output_text.strip()


def critique_answer(model, question, other_answer):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=CRITIQUE_PROMPT.format(
            question=question,
            other_answer=other_answer
        )
    )
    return response.output_text.strip()
