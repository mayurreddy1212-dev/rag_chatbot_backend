from fastapi import FastAPI
from pydantic import BaseModel
from app.tasks import run_agent_task
from app.celery_app import celery
from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.tasks import process_document_task

app = FastAPI()

class QueryRequest(BaseModel):
    session_id: str
    question: str

@app.get("/")
def root():
    return "Status : OK"

@app.post("/chat")
def chat(data: QueryRequest):
    task = run_agent_task.delay(data.session_id, data.question)
    return {"task_id": task.id}

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

    elif task.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task.result)
        }

    else:
        return {"status": task.state}

#upload files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_id = file.filename

    task = process_document_task.delay(file_path, document_id)

    return {"task_id": task.id}
