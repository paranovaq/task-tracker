from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import os


app = FastAPI()

tasks_file = "tasks.json"



class Task(BaseModel):
    id: int
    description: str
    status: str
    created_at: datetime
    updated_at: datetime



class TaskCreate(BaseModel):
    description: str
    status: str = "todo"


def load_tasks() -> list[Task]:
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks: list[Task]):
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1
    now = datetime.now().isoformat()
    new_task = {
        "id": new_id,
        "description": task.description,
        "status": task.status,
        "created_at": now,
        "updated_at": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task