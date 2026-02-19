from app.celery_app import celery

@celery.task(name="app.tasks.run_agent")
def run_agent_task(session_id: str, question: str):
    from app.agent.agent import run_agent
    return run_agent(session_id, question)

from app.celery_app import celery

@celery.task(name="app.tasks.process_document")
def process_document_task(file_path: str, document_id: str):
    from app.agent.document_loader import load_pdf, load_docx, load_txt
    from app.agent.chunker import chunk_text
    from app.agent.vector_store import add_chunk
    import os

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = load_pdf(file_path)
    elif ext == ".docx":
        text = load_docx(file_path)
    elif ext == ".txt":
        text = load_txt(file_path)
    else:
        return "Unsupported file type"

    chunks = chunk_text(text)

    for chunk in chunks:
        add_chunk(document_id, chunk)

    return f"{len(chunks)} chunks processed"
