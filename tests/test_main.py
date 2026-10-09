import os

os.environ["DB_NAME"] = "gestor_tareas_test"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_home():
    response = client.get("/")

    assert response.status_code == 200


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task():
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