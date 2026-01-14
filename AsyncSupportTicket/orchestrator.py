from planner import plan_ticket
from router import route_agent
from executors import draft_only
from approval import requires_approval

async def run_support_agent(ticket: str) -> dict:
    plan = plan_ticket(ticket)
    agent = route_agent(plan)
    draft = await draft_only(plan)

    approval_needed = requires_approval(plan)

    return {
        "plan": plan,
        "agent": agent,
        "draft": draft,
        "approval_required": approval_needed,
        "approved": False
    }
