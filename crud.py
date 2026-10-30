from sqlalchemy.orm import Session

from db_models import TaskDB


def get_all_tasks(db: Session):
    return db.query(TaskDB).all()


def find_task_by_id(db: Session, task_id: int):
    return db.query(TaskDB).filter(TaskDB.id == task_id).first()


def create_task_db(db: Session, title: str, completed: bool):
    task = TaskDB(
        title=title,
        completed=completed
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task_db(db: Session, task_id: int, title: str, completed: bool):
    task = find_task_by_id(db, task_id)

    if task is None:
        return None

    task.title = title
    task.completed = completed

    db.commit()
    db.refresh(task)

    return task


def delete_task_db(db: Session, task_id: int):
    task = find_task_by_id(db, task_id)

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return task