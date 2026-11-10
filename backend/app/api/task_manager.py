from pydantic import BaseModel, Field
from typing import Literal
from fastapi import APIRouter

from task_manager.models import TaskStatus, TaskPriority

from task_manager.storage.json_storage import JSONTaskStorage
from task_manager import TaskManager

task_manager_router = APIRouter()

storage = JSONTaskStorage("tasks.json")

task_manager = TaskManager(storage)

class CreateTaskRequest(BaseModel):
    title: str = Field(description="The title of the task", min_length=5)
    description: str = Field(description="The description of the task", min_length=10)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority | None = TaskPriority.MEDIUM
    
    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "title": "Sample Task",
                "description": "This is a sample task with a description of at least 10 characters",
                "status": "IN_PROGRESS",
                "priority": "MEDIUM"
            }
        }
    }


@task_manager_router.get("/tasks")
def get_tasks():
    return task_manager.get_all_tasks()


@task_manager_router.post("/tasks")
def create_task(task: CreateTaskRequest):
    return task_manager.create_task(**task.dict())