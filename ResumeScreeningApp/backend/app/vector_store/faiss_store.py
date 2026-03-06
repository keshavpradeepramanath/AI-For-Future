import faiss
import numpy as np

class ResumeVectorStore:

    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add_resume(self, embedding, resume_text, filename):

        vector = np.array([embedding]).astype("float32")

        self.index.add(vector)

        self.metadata.append({
            "id": len(self.metadata),
            "resume_text": resume_text,
            "filename": filename
        })


    def search(self, embedding, top_k=20):

        vector = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(vector, top_k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
