from openai import OpenAI
import json

client = OpenAI()

EXTRACTION_PROMPT = """
You are extracting airline baggage rules.

Convert the text below into structured rules.
DO NOT invent rules.
If uncertain, mark decision as "uncertain".

Return JSON ONLY in this format:
[
  {
    "item": "...",
    "decision": "cabin_allowed | checkin_only | not_allowed | uncertain",
    "conditions": "...",
    "reference": "..."
  }
]

TEXT:
{policy_text}
"""

def extract_rules(policy_text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": EXTRACTION_PROMPT.format(policy_text=policy_text)
        }],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
