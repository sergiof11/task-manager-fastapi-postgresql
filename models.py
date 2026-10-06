from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str
    completed: bool


class Task(BaseModel):
    id: int
    title: str
    completed: bool


class TaskDeleteResponse(BaseModel):
    message: str
    id: int
    title: str
    completed: bool