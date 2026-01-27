# agents/preference_agent.py

def interpret_preferences(destination, days, pace, kids, food, budget):
    return {
        "destination": destination,
        "days": days,
        "pace": pace,
        "kids": kids,
        "food_interest": food,
        "budget": budget,
        "daily_activity_limit": (
            2 if pace == "Slow"
            else 3 if pace == "Medium"
            else 5
        )
    }
