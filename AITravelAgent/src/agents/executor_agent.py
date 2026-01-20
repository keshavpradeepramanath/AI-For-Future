from src.prompts.itinerary_prompt import build_itinerary_prompt

class ExecutorAgent:
    def __init__(self, llm, search_tool, logger):
        self.llm = llm
        self.search_tool = search_tool
        self.logger = logger

    def execute(self, plan, user_input):
        self.logger.info("Executor: Executing plan")

        search_context = ""
        if "search" in plan.lower():
            search_context = self.search_tool.search(user_input)

        prompt = build_itinerary_prompt(user_input, search_context)
        return self.llm.invoke(prompt).content
