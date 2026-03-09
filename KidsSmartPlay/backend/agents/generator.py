# backend/agents/generator.py

import random

def game_generator_agent(state):

    day = state.get("day", 1)

    skill = state.get("skill")

    if skill == "counting":

        count = (day % 4) + 2

        objects = ["🍎"] * count

        options = [
            str(count - 1),
            str(count),
            str(count + 1)
        ]

        return {
            **state,
            "game_name": "Fruit Counting",
            "instruction": "Count the apples",
            "question": "How many apples?",
            "objects": objects,
            "options": options,
            "answer": str(count)
        }

    if skill == "pattern recognition":

        patterns = [
            ["🐶","🐱","🐶","🐱"],
            ["🍎","🍌","🍎","🍌"],
            ["🔺","🔵","🔺","🔵"],
        ]

        pattern = patterns[day % len(patterns)]

        return {
            **state,
            "game_name": "Pattern Game",
            "instruction": "Find the next item in the pattern",
            "question": "What comes next?",
            "objects": pattern,
            "options": ["🐶","🐱","🐰"],
            "answer": pattern[0]
        }

    return state
