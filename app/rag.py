from groq import Groq
from app.config import GROQ_API_KEY
import os
from dotenv import load_dotenv
load_dotenv()

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env file")

# Dummy knowledge base
DOCUMENTS = [
    "Redis is an in-memory key value store.",
    "Celery is a distributed task queue.",
    "FastAPI is a modern Python web framework.",
    "RAG stands for Retrieval Augmented Generation."
]

def simple_retriever(query: str):
    for doc in DOCUMENTS:
        if query.lower() in doc.lower():
            return doc
    return DOCUMENTS[0]

def generate_answer(query: str):
    context = simple_retriever(query)

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context}

    Question:
    {query}
    """

    response = GROQ_API_KEY.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Groq hosted model
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
