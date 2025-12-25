from openai import OpenAI

def summarize_email(subject, body):
    client = OpenAI()

    prompt = f"""
Summarize the core purpose of this email in ONE short sentence.

Email subject:
{subject}

Email body:
{body[:3000]}
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return resp.output_text.strip()
