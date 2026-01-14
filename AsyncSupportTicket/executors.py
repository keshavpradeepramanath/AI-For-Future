import asyncio
from mock_agents import billing_agent, tech_agent, general_agent

async def generate_draft(plan):
    if plan["intent"] == "billing":
        return await billing_agent(plan["ticket"])
    elif plan["intent"] == "tech":
        return await tech_agent(plan["ticket"])
    return await general_agent(plan["ticket"])

async def tag_priority(plan):
    await asyncio.sleep(0.5)
    return "P1" if plan["urgency"] == "high" else "P3"

async def draft_only(plan):
    draft, priority = await asyncio.gather(
        generate_draft(plan),
        tag_priority(plan)
    )

    return {
        "draft_response": draft,
        "priority": priority
    }

async def execute_final_action(draft: dict):
    # Mock send action
    return f"✅ Response sent with priority {draft['priority']}"
