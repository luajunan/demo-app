from apscheduler.schedulers.background import BackgroundScheduler
import concurrent.futures
import logging
from app.database import SessionLocal
from app.models import Task
from app.workers import process_task

logger = logging.getLogger(__name__)

def process_pending_tasks():
    db = SessionLocal()
    pending_tasks = db.query(Task).filter(Task.status == "pending").order_by(Task.created_at.asc()).all()
    db.close()

    total_tasks = len(pending_tasks)
    if total_tasks:
        logger.info(f"Scheduler found {total_tasks} pending tasks. Processing with up to 4 concurrent workers.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_task, task) for task in pending_tasks]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    logger.error(f"A task raised an exception: {exc}")
    else:
        logger.info("No pending tasks found by the scheduler.")

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(process_pending_tasks, 'interval', minutes=1, id='process_tasks_job')
    scheduler.start()
    logger.info("Scheduler started.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler shutdown.")
