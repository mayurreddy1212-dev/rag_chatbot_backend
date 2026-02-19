from fastapi import FastAPI
from pydantic import BaseModel
from app.tasks import run_rag
from app.celery_app import celery

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status" : "OK"}

@app.post("/ask")
def ask_question(data: QueryRequest):
    task = run_rag.delay(data.question)
    return {
        "task_id": task.id,
        "status": "processing"
    }

@app.get("/result/{task_id}")
def get_result(task_id: str):
    task = celery.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task.result
        }
    else:
        return {
            "status": task.state
        }
