from .config import load_config

from task_manager.storage.json_storage import JSONTaskStorage
from task_manager import TaskManager

from pathlib import Path

def configure_storage_path(path):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

def create_task_manager():
    """
    Create and return a TaskManager instance based on the configuration.
    The configuration is loaded using the load_config function.
    Currently, only JSON storage is supported.
    """
    
    config = load_config()

    storage_config = config["storage"]

    print(storage_config["type"])
    print(storage_config["path"])
    
    

    if storage_config["type"] == "json":
        configure_storage_path(storage_config["path"])
        storage = JSONTaskStorage(storage_config["path"])
    else:
        raise ValueError(f"Unsupported storage type: {storage_config['type']}")
    
    return TaskManager(storage)
