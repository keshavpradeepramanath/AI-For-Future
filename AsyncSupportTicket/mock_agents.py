import asyncio

async def billing_agent(ticket):
    await asyncio.sleep(1.5)
    return "Billing team response drafted."

async def tech_agent(ticket):
    await asyncio.sleep(2)
    return "Technical troubleshooting steps drafted."

async def general_agent(ticket):
    await asyncio.sleep(1)
    return "General support response drafted."
