from planner import plan_ticket
from router import route_agent
from executors import run_parallel_tasks

async def run_support_agent(ticket: str) -> dict:
    plan = plan_ticket(ticket)
    agent_type = route_agent(plan)
    results = await run_parallel_tasks(plan)

    return {
        "plan": plan,
        "agent_type": agent_type,
        "results": results
    }
