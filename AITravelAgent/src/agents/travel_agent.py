class TravelAgent:
    def __init__(self, planner, executor, critic, logger):
        self.planner = planner
        self.executor = executor
        self.critic = critic
        self.logger = logger

    def run(self, user_input):
        self.logger.info("Starting agentic workflow")

        plan = self.planner.create_plan(user_input)
        draft = self.executor.execute(plan, user_input)
        final_output = self.critic.review(draft)

        return final_output
