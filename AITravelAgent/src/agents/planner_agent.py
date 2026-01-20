class PlannerAgent:
    def __init__(self, llm, logger):
        self.llm = llm
        self.logger = logger

    def create_plan(self, user_input):
        self.logger.info("Planner: Creating plan")

        prompt = f"""
You are a senior AI planner.

User goal:
{user_input}

Create an execution plan.
Return STRICT JSON with:
- steps
- tools_required
- assumptions
"""

        return self.llm.invoke(prompt).content
