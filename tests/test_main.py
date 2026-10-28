import os

os.environ["DB_NAME"] = "gestor_tareas_test"

from fastapi.testclient import TestClient
from main import app
from database import get_connection

client = TestClient(app)


def clear_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks")


def test_get_home():
    response = client.get("/")

    assert response.status_code == 200


def test_get_tasks():
    clear_tasks()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():
    clear_tasks()

    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task():
    clear_tasks()

    response = client.post(
        "/tasks",
        json={
            "title": "Tarea de prueba"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Tarea de prueba"
    assert data["completed"] is False
    assert "id" in data


def test_update_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea original"
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarea actualizada",
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea actualizada"
    assert data["completed"] is True


def test_update_task_not_found():
    clear_tasks()

    response = client.put(
        "/tasks/999999",
        json={
            "title": "No existe",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_get_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para buscar"
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea para buscar"
    assert data["completed"] is False


def test_delete_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para eliminar"
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Tarea eliminada"
    assert data["id"] == task_id
    assert data["title"] == "Tarea para eliminar"
    assert data["completed"] is False


def test_delete_task_not_found():
    clear_tasks()

    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task_with_empty_title():
    clear_tasks()

    response = client.post(
        "/tasks",
        json={
            "title": "     "
        }
    )

    assert response.status_code == 422