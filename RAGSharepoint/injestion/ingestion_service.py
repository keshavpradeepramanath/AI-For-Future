from ingestion.sharepoint_loader import SharePointLoader

class IngestionService:
    def __init__(self, loader, vector_store):
        self.loader = loader
        self.vector_store = vector_store

    def ingest(self):
        documents = self.loader.list_documents()

        for doc in documents:
            text = self.loader.load_document_content(doc)

            self.vector_store.add({
                "text": text,
                "source": f"{doc['name']} ({doc['path']})"
            })
