import asyncio
from mock_agents import billing_agent, tech_agent, general_agent

async def assign_team(intent):
    await asyncio.sleep(0.5)
    return f"{intent.capitalize()} Support Team"

async def tag_priority(urgency):
    await asyncio.sleep(0.5)
    return "P1" if urgency == "high" else "P3"

async def generate_response(plan):
    if plan["intent"] == "billing":
        return await billing_agent(plan["ticket"])
    elif plan["intent"] == "tech":
        return await tech_agent(plan["ticket"])
    return await general_agent(plan["ticket"])

async def run_parallel_tasks(plan):
    response, team, priority = await asyncio.gather(
        generate_response(plan),
        assign_team(plan["intent"]),
        tag_priority(plan["urgency"])
    )

    return {
        "draft_response": response,
        "assigned_team": team,
        "priority": priority
    }
