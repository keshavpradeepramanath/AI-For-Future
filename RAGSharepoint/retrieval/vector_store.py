class InMemoryVectorStore:
    """
    Placeholder for FAISS / Pinecone / Weaviate.
    """

    def __init__(self):
        self.data = []

    def add(self, chunk: dict):
        self.data.append(chunk)

    def search(self, query: str, top_k: int):
        # mock relevance
        return self.data[:top_k]
