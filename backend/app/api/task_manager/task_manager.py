from pydantic import BaseModel, Field
from typing import Literal, Optional
from fastapi import HTTPException
from fastapi import APIRouter
from .mapping import STATUS_MAPPING, PRIORITY_MAPPING
from starlette import status

from .config import load_config

from .init_task_manager import create_task_manager
from task_manager import Task, TaskFilter

task_manager_router = APIRouter()
task_manager = create_task_manager()

class CreateTaskRequest(BaseModel):

    # id: Optional[int] = Field(description="The ID of the task; Needed for updates only")
    title: str = Field(description="The title of the task", min_length=5, pattern=r"\S")
    description: str = Field(description="The description of the task", min_length=10, pattern=r"\S")
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
def get_tasks(priority: Literal["URGENT", "HIGH", "MEDIUM", "LOW"] = None, 
              status: Literal["TODO", "IN_PROGRESS", "DONE"] = None):
    
    filter = TaskFilter()
    filter.priority = PRIORITY_MAPPING[priority] if priority in PRIORITY_MAPPING else None  
    filter.status = STATUS_MAPPING[status] if status in STATUS_MAPPING else None
        
    return task_manager.get_all_tasks(filter=filter)


@task_manager_router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTaskRequest):
    return task_manager.create_task(
        title=task.title,
        description=task.description,
        status=STATUS_MAPPING[task.status],
        priority=PRIORITY_MAPPING[task.priority]
    )
    
@task_manager_router.put("/tasks/{task_id}", status_code=status.HTTP_202_ACCEPTED)
def update_task(task_id: int, task: CreateTaskRequest):
    try:
        return task_manager.update_task(
            task_id=task_id,
            task=Task(
                id=task_id,
                title=task.title,
                description=task.description,
                status=STATUS_MAPPING[task.status],
                priority=PRIORITY_MAPPING[task.priority],
            ),
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) 
    

@task_manager_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    try:
        task_manager.delete_task(task_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) 