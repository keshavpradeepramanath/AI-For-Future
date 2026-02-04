from core.interfaces import Retriever
from retrieval.vector_store import InMemoryVectorStore
from config.settings import SETTINGS

class HybridRetriever(Retriever):
    def __init__(self, vector_store: InMemoryVectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str):
        results = self.vector_store.search(
            query=query,
            top_k=SETTINGS.MAX_CONTEXT_CHUNKS
        )
        return results
