from openai import OpenAI
from prompts import JUDGE_PROMPT
import json

def judge_answers(question, answers):
    client = OpenAI()

    formatted = ""
    for model, ans in answers.items():
        formatted += f"{model}: {ans}\n\n"

    resp = client.responses.create(
        model="gpt-4o",
        input=JUDGE_PROMPT + "\n" + formatted
    )

    return resp.output_text
