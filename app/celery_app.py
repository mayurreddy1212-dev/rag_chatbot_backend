from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "rag_chatbot",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.autodiscover_tasks(["app"])

