from pydantic import BaseModel

class TaskRequest(BaseModel):
    description: str
