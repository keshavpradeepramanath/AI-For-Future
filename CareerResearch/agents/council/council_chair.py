from services.llm_clients.openai_client import call_gpt_async

async def synthesize_council(council_inputs: dict) -> str:
    prompt = f"""
You are the chair of an expert LLM council.

Below are opinions from multiple personas and models:
{council_inputs}

Produce ONE unified career roadmap.

Use EXACT headings:
## Role Expectations
## Required Skillsets
## Learning Roadmap
## Career Risks & Practical Advice
"""
    return await call_gpt_async(prompt, temperature=0.2)
