from database import cursor, conn


def find_task_by_id(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


def get_all_tasks():
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

    conn.commit()

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }

def delete_task_db(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()


def update_task_db(task_id: int, title: str, completed: bool):
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

    conn.commit()

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }