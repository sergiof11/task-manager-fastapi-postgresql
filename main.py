from fastapi import FastAPI, HTTPException

from models import TaskCreate, TaskUpdate
from crud import (
    find_task_by_id,
    get_all_tasks,
    create_task_db,
    delete_task_db,
    update_task_db
)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API funcionando"}


@app.get("/tasks") 
def get_tasks():
    tasks = get_all_tasks()
    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return {"task": task}


@app.post("/tasks")
def create_task(task: TaskCreate):
    create_task_db(task.title, task.completed)
    return {"message": "Tarea creada"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = find_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    delete_task_db(task_id)
    return {"message": "Tarea eliminada"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    existing_task = find_task_by_id(task_id)

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_task_db(task_id, task.title, task.completed)
    return {"message": "Tarea actualizada"}