import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a hiring assistant."},
                {"role": "user", "content": prompt[:12000]}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "Score: 0\nDecision: REJECT\nReasoning: LLM error\nSummary: "
