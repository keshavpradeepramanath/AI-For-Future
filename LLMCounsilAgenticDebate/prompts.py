ANSWER_PROMPT = """
You are an expert AI assistant.

Answer the following question clearly and accurately.
Avoid unnecessary verbosity.

Question:
{question}
"""

CRITIQUE_PROMPT = """
You are reviewing answers from other AI systems.

Your task:
- Point out inaccuracies or missing details
- Highlight strengths and weaknesses
- Be objective and concise

Original question:
{question}

Other answer:
{other_answer}
"""

JUDGE_PROMPT = """
You are an impartial judge comparing multiple AI answers.

Your task:
- Decide which answer best addresses the question
- Explain why it is the closest or most accurate
- Choose ONE winner

Question:
{question}

Answers:
{answers}
"""
