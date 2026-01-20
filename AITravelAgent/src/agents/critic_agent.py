class CriticAgent:
    def __init__(self, llm, logger):
        self.llm = llm
        self.logger = logger

    def review(self, itinerary):
        self.logger.info("Critic: Reviewing itinerary")

        prompt = f"""
You are a critical travel expert.

Review the itinerary below:
{itinerary}

Check:
- Feasibility
- Travel times
- Fatigue
- Logical flow

If problems exist, FIX them.
Otherwise return as-is.
"""

        return self.llm.invoke(prompt).content
