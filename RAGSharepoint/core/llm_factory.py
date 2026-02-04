from core.interfaces import LLM
from config.secrets import Secrets

class OpenAILLM(LLM):
    def generate(self, prompt: str) -> str:
        # placeholder for actual SDK call
        return f"[OpenAI] {prompt[:200]}"


class ClaudeLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Claude] {prompt[:200]}"


class GeminiLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Gemini] {prompt[:200]}"


class LLMFactory:
    @staticmethod
    def create(provider: str) -> LLM:
        if provider == "openai":
            return OpenAILLM()
        if provider == "claude":
            return ClaudeLLM()
        if provider == "gemini":
            return GeminiLLM()
        raise ValueError(f"Unsupported LLM provider: {provider}")
