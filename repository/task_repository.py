import json
import os
from models.task import Task

tasks_file = "tasks.json"

def load_tasks() -> list[Task]:
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, "r", encoding="utf-8") as f:
        try:
            tasks_data = json.load(f)
            return [Task(**task) for task in tasks_data]
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: list[Task]):
    tasks_data = [task.model_dump() for task in tasks]
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, indent=2, ensure_ascii=False, default=str)
