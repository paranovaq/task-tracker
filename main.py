from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()
tasks_file = "tasks.json"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
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

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate, status: TaskStatus = None):
    tasks = load_tasks()
    task_to_update = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_update = task
            break
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")
    task_to_update["description"] = task_update.description
    if status:
        task_to_update["status"] = status.value
    task_to_update["updated_at"] = datetime.now().isoformat()
    save_tasks(tasks)
    return task_to_update

