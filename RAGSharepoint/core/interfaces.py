from abc import ABC, abstractmethod
from typing import List

class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> List[dict]:
        pass
