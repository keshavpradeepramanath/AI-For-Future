from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_batch(skill):

    prompt = f"""


    You are an expert child psychologist designing visual exercises for 5-year-old children.

    IMPORTANT:
    Children cannot read well. Exercises must be VISUAL using emojis.

    Skill category: {skill}

    Allowed activity types:

    * count objects
    * find the odd one
    * match pairs
    * identify biggest/smallest
    * color grouping
    * memory recall
    * shadow matching
    * object classification
    * emotion recognition
    * simple maze direction
    * pattern completion
    * object comparison

    Rules:

    * Exercises must be very visual
    * Avoid repeating the same activity type
    * Use different emojis each time
    * Keep instructions short

    Each exercise must contain:

    game_name
    instruction
    objects
    options
    answer

    Return JSON only in this format:

    {{
    "exercises":[
    {{
    "game_name":"Find the Odd Animal",
    "instruction":"Find the different animal",
    "objects":["🐶","🐶","🐱","🐶"],
    "options":["🐶","🐱"],
    "answer":"🐱"
    }}
    ]
    }}
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.9,
        response_format={"type":"json_object"}
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    return data.get("exercises", [])


def generate_curriculum():


    categories = [
        "observation and attention",
        "memory and recall",
        "logic and reasoning",
        "basic math and counting",
        "creativity and imagination"
    ]

    exercises = []

    print("Generating diverse visual exercises...")

    for category in categories:

        batch = []

        while len(batch) < 20:

            new_items = generate_batch(category)

            batch.extend(new_items)

        batch = batch[:20]

        print(category, ":", len(batch))

        exercises.extend(batch)

    print("Total exercises:", len(exercises))

    return exercises

