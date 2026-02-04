from core.prompts import SYSTEM_PROMPT
from config.settings import SETTINGS

class RAGEngine:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def answer(self, query: str) -> dict:
        chunks = self.retriever.retrieve(query)

        if not chunks:
            return {
                "answer": "I don’t see this covered in the available material.",
                "sources": []
            }

        context = "\n\n".join(
            f"{c['text']} (Source: {c['source']})"
            for c in chunks
        )

        prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}
"""

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": [c["source"] for c in chunks]
        }
