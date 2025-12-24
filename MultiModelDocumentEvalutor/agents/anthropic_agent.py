import anthropic
from prompts import EXTRACTION_PROMPT


def run_claude(context, question, model_name="claude-3-sonnet-20240229"):
    """
    Runs document extraction / QnA using Anthropic Claude (direct API).
    """
    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY

    prompt = EXTRACTION_PROMPT.format(
        context=context,
        question=question
    )

    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text.strip()
