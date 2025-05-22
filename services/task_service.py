from datetime import datetime
from typing import Optional
from models.task import Task, TaskStatus
from repository.task_repository import load_tasks, save_tasks


def get_tasks(status: Optional[TaskStatus] = None) -> list[Task]:
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task.status == status]
    return tasks


def create_task(task_name: str) -> Task:
    tasks = load_tasks()
    new_id = max([task.id for task in tasks], default=0) + 1
    now = datetime.now()
    new_task = Task(
        id=new_id,
        description=task_name,
        status=TaskStatus.TODO,
        created_at=now,
        updated_at=now
    )
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def update_task(task_id: int, task_name: str, status: TaskStatus) -> Task:
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.description = task_name
            t.status = status
            t.updated_at = datetime.now()
            save_tasks(tasks)
            return t
    raise ValueError("Task not found")


def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task.id != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks)
    return True


def change_task_status(task_id: int, status: TaskStatus) -> Task:
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.status = status
            task.updated_at = datetime.now()
            save_tasks(tasks)
            return task
    raise ValueError("Task not found")
