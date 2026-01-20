from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class LLMFactory:
    @staticmethod
    def create(provider, model):
        if provider == "groq":
            return ChatGroq(model=model)
        elif provider == "openai":
            return ChatOpenAI(model=model)
        else:
            raise ValueError("Unsupported LLM provider")
