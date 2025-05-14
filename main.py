from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()
tasks_file = "tasks.json"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    DONE = "done"

class TaskCreate(BaseModel):
    description: str

class Task(BaseModel):
    id: int
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

def load_tasks() -> list[dict]:
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: list[dict]):
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False, default=str)

@app.get("/tasks/", response_model=list[Task])
async def get_tasks(status: TaskStatus = None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status.value]
    return tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    tasks = load_tasks()
    new_id = max([task.get("id", 0) for task in tasks], default=0) + 1
    now = datetime.now().isoformat()
    new_task = {
        "id": new_id,
        "description": task.description,
        "status": TaskStatus.TODO.value,
        "created_at": now,
        "updated_at": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


