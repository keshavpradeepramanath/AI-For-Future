from openai import OpenAI

def normalize_sender(sender_text):
    client = OpenAI()

    prompt = f"""
Extract the company or brand name from the sender.

Examples:
- "ICICI Bank <alerts@icicibank.com>" → ICICI
- "MakeMyTrip Deals <offers@makemytrip.com>" → MakeMyTrip
- "Tata Neu <no-reply@tata.com>" → Tata

Sender:
{sender_text}

Return ONLY the company name.
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return resp.output_text.strip()
