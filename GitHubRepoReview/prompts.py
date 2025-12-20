REVIEW_PROMPT = """
You are a senior software engineer performing a code review.

File: {file_path}

Code:
{code}

Tasks:
1. Identify bugs or code smells
2. Point out design and readability issues
3. Suggest concrete refactors
4. Explain why each suggestion matters

Be concise and professional.
"""
