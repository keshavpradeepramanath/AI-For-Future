from openai import OpenAI
from prompts import CLASSIFY_EMAIL_PROMPT

def classify_email(subject, sender, body):
    client = OpenAI()

    prompt = CLASSIFY_EMAIL_PROMPT.format(
        subject=subject,
        sender=sender,
        body=body[:1000]  # safety limit
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text.strip()
