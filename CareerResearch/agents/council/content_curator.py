from services.llm_router import call_all_models_async

async def curate_learning_content_async(target_role: str, skills: str):
    prompt = f"""
You are a senior learning content curator.

Target role:
{target_role}

Required skills:
{skills}

Task:
Recommend EXACTLY:
- Top 3 FREE resources (YouTube only)
- Top 3 PAID resources (Coursera, Udemy, edX, Harvard, etc.)

STRICT RULES:
- Prefer courses with HIGH ratings (4.5+)
- Prefer courses with LARGE learner base (100k+ where applicable)
- Prefer well-known instructors or institutions
- Avoid obscure or low-adoption content
- No imaginary or niche courses

For EACH course include:
- Title
- Platform
- Instructor / Institution
- Approx rating
- Approx number of learners
- Why it is ranked in top 3

Output format MUST be:

FREE RESOURCES:
1. ...
2. ...
3. ...

PAID RESOURCES:
1. ...
2. ...
3. ...
"""
    return await call_all_models_async(prompt)
