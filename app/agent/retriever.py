from app.agent.vector_store import search

def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Retrieve top relevant chunks from vector store.
    """
    results = search(query, top_k=top_k)

    if not results:
        return ""

    return "\n\n".join(results)