import logging
from fastapi import FastAPI, HTTPException, Request
from app.database import engine, SessionLocal
from app import models, crud, scheduler
from app.schemas import TaskRequest

# Set up logging configuration
logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create all tables in the database (if not already created)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tasks")
def create_task(task: TaskRequest, request: Request):
    client_ip = request.client.host
    db = SessionLocal()
    new_task = crud.create_task(db, task)
    db.close()
    logger.info(f"Task created: task_id={new_task.id} from IP {client_ip}")
    return {"task_id": new_task.id, "status": new_task.status}

@app.get("/results")
def get_task(task_id: int):
    db = SessionLocal()
    task_data = crud.get_task_result(db, task_id)
    db.close()
    if task_data is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_data

@app.get("/metrics")
def get_metrics():
    db = SessionLocal()
    metrics = crud.get_metrics_results(db)
    db.close()
    return metrics

@app.on_event("startup")
def startup_event():
    scheduler.start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
