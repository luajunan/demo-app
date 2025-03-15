import time
import random
from app.database import SessionLocal
from app.models import Task
import logging

logger = logging.getLogger(__name__)

def predict(task_id: int, description: str) -> str:
    # Simulate an ML prediction (replace with your model inference)
    time.sleep(2)  # simulate processing delay
    return f"Prediction for task {task_id}: {random.choice(['A', 'B', 'C'])}"

def process_task(task: Task):
    db = SessionLocal()
    # Re-fetch the task to ensure it is still pending
    task_in_db = db.query(Task).filter(Task.id == task.id, Task.status == "pending").first()
    if task_in_db:
        logger.info(f"Task {task_in_db.id} claimed and marked as processing.")
        task_in_db.status = "processing"
        db.commit()
        db.refresh(task_in_db)

        # Log start of processing
        logger.info(f"Task {task_in_db.id} started processing.")

        # Run prediction
        result = predict(task_in_db.id, task_in_db.description)

        # Update task with result and mark as completed
        task_in_db.result = result
        task_in_db.status = "completed"
        db.commit()
        db.refresh(task_in_db)
        logger.info(f"Task {task_in_db.id} completed processing with result: {result}.")
    db.close()
