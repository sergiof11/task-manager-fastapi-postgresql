from database import get_connection


def find_task_by_id(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tasks WHERE id = %s",
                (task_id,)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        })

    return tasks


def create_task_db(title: str, completed: bool):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, completed)
                VALUES (%s, %s)
                RETURNING id, title, completed
                """,
                (title, completed)
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("No se pudo crear la tarea")

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


def delete_task_db(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id, title, completed
                """,
                (task_id,)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


def update_task_db(task_id: int, title: str, completed: bool):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, completed = %s
                WHERE id = %s
                RETURNING id, title, completed
                """,
                (title, completed, task_id)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }