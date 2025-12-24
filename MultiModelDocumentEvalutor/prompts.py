EXTRACTION_PROMPT = """
You are an information extraction expert.

Answer the user's question strictly using the provided document.
Dont hallucinate.
If the answer is not present, say "Not found in document".

Document:
{context}

Question:
{question}
"""

JUDGE_PROMPT = """
You are evaluating answers from multiple AI models.

Tasks:
1. Score each answer for factual accuracy (0-10)
2. Score consistency with other answers (0-10)
3. Identify the best overall answer

Return results in the below format :
- model_name
- accuracy_score
- consistency_score
- reasoning
"""
