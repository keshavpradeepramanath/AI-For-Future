from openai import OpenAI
from prompts import PROMPT_REFINER_SYSTEM


def refine_prompt(user_prompt: str) -> str:
    """
    Takes a basic user prompt and returns a clearer,
    more detailed, high-quality prompt.
    """
    client = OpenAI()

    messages = [
        {"role": "system", "content": PROMPT_REFINER_SYSTEM},
        {"role": "user", "content": user_prompt}
    ]

    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=messages
    )

    return response.output_text.strip()
