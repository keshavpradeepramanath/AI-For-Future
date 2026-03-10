from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_batch():


    prompt = """


    Generate EXACTLY 20 learning exercises for a 5 year old.

    Each exercise must include:

    game_name
    instruction
    question
    objects
    options
    answer

    Return JSON only in this format:

    {
    "exercises":[
    {
    "game_name":"Fruit Counting",
    "instruction":"Count the apples",
    "question":"How many apples?",
    "objects":["🍎","🍎","🍎"],
    "options":["2","3","4"],
    "answer":"3"
    }
    ]
    }
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7,
        response_format={"type":"json_object"}
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    exercises = data.get("exercises", [])

    return exercises


def generate_curriculum():

    exercises = []

    print("Generating exercises using LLM...")

    while len(exercises) < 100:

        batch = generate_batch()

        print("Received batch:", len(batch))

        exercises.extend(batch)

        print("Total so far:", len(exercises))

    return exercises[:100]

