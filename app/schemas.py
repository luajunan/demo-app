from pydantic import BaseModel

class TaskRequest(BaseModel):
    description: str

class Metrics(BaseModel):
    pending_tasks: int
    completed_tasks: int