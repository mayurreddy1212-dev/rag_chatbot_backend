DOCUMENTS = [
    "Redis is an in-memory key value store.",
    "Celery is a distributed task queue.",
    "FastAPI is a modern Python web framework.",
    "RAG stands for Retrieval Augmented Generation."
]

def retrieve_docs(query: str):
    for doc in DOCUMENTS:
        if query.lower() in doc.lower():
            return doc
    return DOCUMENTS[0]
