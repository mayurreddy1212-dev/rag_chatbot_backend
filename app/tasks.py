from app.celery_app import celery
from app.agent.agent import run_agent

@celery.task(name="app.tasks.run_agent")
def run_agent_task(session_id: str, question: str):
    return run_agent(session_id, question)
