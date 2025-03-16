from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskRequest, Metrics

def create_task(db: Session, task_request: TaskRequest) -> Task:
    db_task = Task(description=task_request.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_pending_tasks(db: Session):
    return db.query(Task).filter(Task.status == "pending").all()

def update_task_status(db: Session, task_id: int, new_status: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = new_status
        db.commit()
        db.refresh(task)
    return task

def complete_task(db: Session, task_id: int, result: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.result = result
        task.status = "completed"
        db.commit()
        db.refresh(task)
    return task

def get_task_result(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        return {"search_results": {"task_id": task_id, "tasking_status": task.status, "prediction_result": task.result}}
    else:
        return None

def get_metrics_results(db: Session):
    pending_tasks = db.query(Task).filter(Task.status == "pending").count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    metrics = Metrics(pending_tasks=pending_tasks, completed_tasks=completed_tasks)
    return metrics
