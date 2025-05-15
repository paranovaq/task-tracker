from fastapi import APIRouter, HTTPException
from models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from services import task_service


router = APIRouter()

@router.get("/tasks/", response_model=list[Task])
def read_tasks(status: TaskStatus = None):
    return task_service.get_tasks(status)

@router.post("/tasks/", response_model=Task)
def create_task(task_data: TaskCreate):
    return task_service.create_task(task_data)

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, status: TaskStatus):
    try:
        return task_service.update_task(task_id, task_data, status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/status", response_model=Task)
def change_status(task_id: int, status: TaskStatus):
    try:
        return task_service.change_task_status(task_id, status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
