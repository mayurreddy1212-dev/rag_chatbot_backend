import redis
import json
import numpy as np
import uuid
from app.config import REDIS_URL
from app.agent.embeddings import get_embedding

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def add_chunk(document_id: str, text: str):
    embedding = get_embedding(text)

    chunk_id = str(uuid.uuid4())

    r.set(f"chunk:{chunk_id}", json.dumps({
        "document_id": document_id,
        "text": text,
        "embedding": embedding
    }))

def get_all_chunks():
    keys = r.keys("chunk:*")
    chunks = []
    for key in keys:
        chunks.append(json.loads(r.get(key)))
    return chunks

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query: str, top_k=3):
    query_embedding = get_embedding(query)
    chunks = get_all_chunks()

    scored = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append((score, chunk["text"]))

    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]
