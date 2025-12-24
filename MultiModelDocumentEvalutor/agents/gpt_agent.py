from openai import OpenAI
from prompts import EXTRACTION_PROMPT

def run_gpt(context, question):
    client = OpenAI()
    prompt = EXTRACTION_PROMPT.format(
        context=context,
        question=question
    )

    resp = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    return resp.output_text.strip()
