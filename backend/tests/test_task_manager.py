from fastapi.testclient import TestClient
import pytest
from task_manager import TaskManager
from task_manager.storage.json_storage import JSONTaskStorage

from backend.app.main import app
from backend.app.api.task_manager import task_manager as task_manager_api

@pytest.mark.parametrize("origin", 
                         ["http://localhost:5500",
                        "http://127.0.0.1:5500",
                        "https://beyond-main.andrei-baciu94.workers.dev"],
)
def test_task_update_cors_preflight(origin):
    client = TestClient(app)
    response = client.options(
        "/tasks-manager/tasks/1",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    
@pytest.mark.parametrize("method",
                         ["GET", "POST", "PUT", "DELETE"])
def test_task_update_cors_preflight_methods(method):
    client = TestClient(app)
    response = client.options(
        "/tasks-manager/tasks/1",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    
    allowed_methods = response.headers["access-control-allow-methods"].split(", ")
    assert method in allowed_methods
    

def test_task_create_list_and_update(tmp_path, monkeypatch):
    manager = TaskManager(JSONTaskStorage(str(tmp_path / "tasks.json")))
    monkeypatch.setattr(task_manager_api, "task_manager", manager)
    client = TestClient(app)
    task = {
        "title": "First task",
        "description": "A task description",
        "status": "TODO",
        "priority": "MEDIUM",
    }

    created = client.post("/tasks-manager/tasks", json=task)
    assert created.status_code == 201
    
    task_id = created.json()["id"]

    task.update(title="Updated task", status="IN_PROGRESS", priority="HIGH")
    updated = client.put(f"/tasks-manager/tasks/{task_id}", json=task)
    assert updated.status_code == 202
    assert client.get("/tasks-manager/tasks").json() == [{
        "id": task_id,
        **task,
        "priority": 1,
    }]
    
def test_task_delete(tmp_path, monkeypatch):
    manager = TaskManager(JSONTaskStorage(str(tmp_path / "tasks.json")))
    monkeypatch.setattr(task_manager_api, "task_manager", manager)
    client = TestClient(app)
    task = {
        "title": "Task to delete",
        "description": "A task description",
        "status": "TODO",
        "priority": "MEDIUM",
    }
    created = client.post("/tasks-manager/tasks", json=task)
    assert created.status_code == 201
    task_id = created.json()["id"]

    response = client.delete(f"/tasks-manager/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get("/tasks-manager/tasks").json() == []
    
    # try to delete the same task again should return 404
    response = client.delete(f"/tasks-manager/tasks/{task_id}")
    assert response.status_code == 404

def test_create_task_invalid_task(tmp_path, monkeypatch):
    manager = TaskManager(JSONTaskStorage(str(tmp_path / "tasks.json")))
    monkeypatch.setattr(task_manager_api, "task_manager", manager)
    client = TestClient(app)
    invalid_task = {
        "title": "",
        "description": "A task description",
        "status": "TODO",
        "priority": "MEDIUM",
    }
    
    # create task with invalid title
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]
    assert response.json()["detail"][0]["msg"] == "String should have at least 5 characters"
    
    # create task with title too short
    invalid_task["title"] = "1234"
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]
    assert response.json()["detail"][0]["msg"] == "String should have at least 5 characters"

    # create task with description too short
    invalid_task["title"] = "Valid title"
    invalid_task["description"] = ""
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "description"]
    assert response.json()["detail"][0]["msg"] == "String should have at least 10 characters"

    # create task with invalid status
    invalid_task["description"] = "Valid description"
    invalid_task["status"] = "INVALID_STATUS"
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "status"]
    assert response.json()["detail"][0]["msg"] == "Input should be 'TODO', 'IN_PROGRESS' or 'DONE'"

    # create task with invalid priority
    invalid_task["status"] = "TODO"
    invalid_task["priority"] = "INVALID_PRIORITY"
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "priority"]
    assert response.json()["detail"][0]["msg"] == "Input should be 'URGENT', 'HIGH', 'MEDIUM' or 'LOW'"

    # create task with valid data
    invalid_task["priority"] = "LOW"
    response = client.post("/tasks-manager/tasks", json=invalid_task)
    assert response.status_code == 201
    assert response.json()["title"] == "Valid title"
    assert response.json()["description"] == "Valid description"
    assert response.json()["status"] == "TODO"
    assert response.json()["priority"] == 3
    assert "id" in response.json()