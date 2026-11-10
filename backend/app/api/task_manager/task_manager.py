from pydantic import BaseModel, Field
from typing import Literal
from fastapi import APIRouter
from .mapping import STATUS_MAPPING, PRIORITY_MAPPING
from starlette import status

from .config import load_config

from .init_task_manager import create_task_manager

task_manager_router = APIRouter()
task_manager = create_task_manager()

class CreateTaskRequest(BaseModel):
    title: str = Field(description="The title of the task", min_length=5)
    description: str = Field(description="The description of the task", min_length=10)
    status: Literal["TODO", "IN_PROGRESS", "DONE"] = "TODO"
    priority: Literal["URGENT", "HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    
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


@task_manager_router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks():
    return task_manager.get_all_tasks()


@task_manager_router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTaskRequest):
    return task_manager.create_task(
        title=task.title,
        description=task.description,
        status=STATUS_MAPPING[task.status],
        priority=PRIORITY_MAPPING[task.priority]
    )
    
    