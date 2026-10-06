from fastapi import FastAPI, HTTPException

from models import Task, TaskCreate, TaskUpdate, TaskDeleteResponse

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


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    tasks = get_all_tasks()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = find_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = create_task_db(task.title, task.completed)
    return new_task


@app.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
def delete_task(task_id: int):
    task = find_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    delete_task_db(task_id)

    return {
        "message": "Tarea eliminada",
        "id": task["id"],
        "title": task["title"],
        "completed": task["completed"]
    }

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    existing_task = find_task_by_id(task_id)

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    updated_task = update_task_db(task_id, task.title, task.completed)

    return updated_task