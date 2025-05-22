from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

class Task(BaseModel):
    id: int
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

