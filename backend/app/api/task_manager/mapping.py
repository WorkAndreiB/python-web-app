from task_manager.models import TaskStatus, TaskPriority

STATUS_MAPPING ={
    "TODO": TaskStatus.TODO,
    "IN_PROGRESS": TaskStatus.IN_PROGRESS,
    "DONE": TaskStatus.DONE
}

PRIORITY_MAPPING = {
    "URGENT": TaskPriority.URGENT,
    "HIGH": TaskPriority.HIGH,
    "MEDIUM": TaskPriority.MEDIUM,
    "LOW": TaskPriority.LOW
}
