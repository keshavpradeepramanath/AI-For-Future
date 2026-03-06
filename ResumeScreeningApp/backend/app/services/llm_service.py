import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def call_llm(prompt):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},   # <-- forces valid JSON
        messages=[
            {
                "role": "system",
                "content": "You are an expert recruiter evaluating resumes against job descriptions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
