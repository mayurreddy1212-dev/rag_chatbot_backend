from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.tasks import run_agent_task
from app.celery_app import celery
from fastapi import FastAPI, UploadFile, File, Depends
import shutil
import os
from app.tasks import process_document_task
from app.agent.vector_store import list_documents, count_documents, delete_document
from app.database import get_db
from app.models import Document
from app.schemas import DocumentResponse
from app.agent.vector_store import delete_document as delete_from_redis
from sqlalchemy.orm import Session
from typing import List
from app.database import engine
from app.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

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
def upload_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    uploaded_docs = []

    for file in files:
        #Save file to disk
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        #Save metadata to DB
        doc = Document(filename=file.filename)
        db.add(doc)
        db.commit()
        db.refresh(doc)

        #Send to Celery with document_id
        process_document_task.delay(doc.id, file_path)

        uploaded_docs.append({
            "document_id": doc.id,
            "filename": doc.filename
        })

    return {
        "status": "processing_started",
        "documents": uploaded_docs
    }

@app.get("/documents", response_model=List[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents

@app.delete("/documents/{document_id}")
def delete_document_route(document_id: int, db: Session = Depends(get_db)):

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_from_redis(str(document_id))

    file_path = os.path.join(UPLOAD_DIR, document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(document)
    db.commit()

    return {"status": "deleted", "document_id": document_id}