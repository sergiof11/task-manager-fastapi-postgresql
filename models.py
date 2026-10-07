from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("El título no puede estar vacío")

        return value


class TaskCreate(TaskBase):
    completed: bool = False


class TaskUpdate(TaskBase):
    completed: bool


class Task(TaskBase):
    id: int
    completed: bool


class TaskDeleteResponse(TaskBase):
    message: str
    id: int
    completed: bool