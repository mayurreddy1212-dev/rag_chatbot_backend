from app.celery_app import celery
from app.rag import generate_answer

@celery.task(name="app.tasks.run_rag")
def run_rag(query: str):
    result = generate_answer(query)
    return result
