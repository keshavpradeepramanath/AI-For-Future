from services.llm_clients.openai_client import call_gpt

def synthesize_council(council_inputs: dict) -> str:
    prompt = f"""
You are the chair of an expert LLM council.

Below are opinions from multiple models and personas:
{council_inputs}

Your task:
1. Identify agreements
2. Resolve disagreements
3. Produce ONE unified career roadmap

Output sections:
- Role Expectations
- Required Skillsets
- Learning Roadmap
- Career Risks & Advice
"""
    return call_gpt(prompt, temperature=0.2)
