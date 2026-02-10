from services.llm_clients.openai_client import call_gpt_async

async def generate_60_day_roadmap(
    career_plan: str,
    gap_analysis: str,
    resume_improvements: str
) -> str:
    prompt = f"""
You are a senior career coach and execution planner.

TARGET CAREER PLAN:
{career_plan}

RESUME GAP ANALYSIS:
{gap_analysis}

RESUME IMPROVEMENTS:
{resume_improvements}

Task:
Create a PRACTICAL 60-day execution roadmap.

Rules:
- Break into Weeks (Week 1 to Week 8)
- Each week must have 3–5 concrete tasks
- Tasks must be:
  - Skill-building
  - Resume-improving
  - Interview-prep where relevant
- Avoid generic advice

Output FORMAT (STRICT):

Week X:
- Task:
  Skill Focus:
  Estimated Effort (hours):
  Outcome:

Do NOT add extra sections.
"""
    return await call_gpt_async(prompt, temperature=0.2)
