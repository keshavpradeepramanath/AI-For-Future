import os

class Secrets:
    @staticmethod
    def openai_key() -> str:
        return os.getenv("OPENAI_API_KEY")

    @staticmethod
    def claude_key() -> str:
        return os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def gemini_key() -> str:
        return os.getenv("GEMINI_API_KEY")
