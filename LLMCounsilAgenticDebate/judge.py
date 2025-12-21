from openai import OpenAI
from prompts import JUDGE_PROMPT

def judge_answers(question, answers_dict):
    client = OpenAI()

    formatted_answers = ""
    for name, ans in answers_dict.items():
        formatted_answers += f"{name}:\n{ans}\n\n"

    response = client.responses.create(
        model="gpt-4o",
        input=JUDGE_PROMPT.format(
            question=question,
            answers=formatted_answers
        )
    )

    return response.output_text.strip()
