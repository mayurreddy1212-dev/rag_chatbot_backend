from groq import Groq
from app.config import GROQ_API_KEY
from app.agent.retriever import retrieve_context

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(query: str):

    #Retrieve context from vector store
    context = retrieve_context(query)

    if not context:
        return "No relevant documents found in knowledge base."

    #Build prompt
    prompt = f"""
You are a helpful AI assistant. 
Answer the question ONLY using the provided context.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{query}
"""

    #Call Groq LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You answer based only on provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content