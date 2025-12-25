from openai import OpenAI

LABELS = [
    "Promotional",
    "Bank Statement",
    "Due Payment",
    "Trip Suggestion",
    "Account Update",
    "Other"
]

def classify_intent(summary):
    client = OpenAI()

    prompt = f"""
Classify the email intent into ONE of the following labels:

{LABELS}

Email summary:
{summary}

Return ONLY the label.
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    label = resp.output_text.strip()

    return label if label in LABELS else "Other"
