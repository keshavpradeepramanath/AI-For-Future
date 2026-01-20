def build_itinerary_prompt(user_input, search_context):
    return f"""
You are a professional travel itinerary planner.

User requirements:
{user_input}

Real-time travel information:
{search_context}

Generate a detailed, realistic, day-by-day itinerary.
Include:
- Places
- Activities
- Travel time buffers
- Food suggestions
- Rest periods
- Make it kids friends as well.
"""
