# Task Manager API

FastAPI router that exposes the `task_manager` Python package (from the `python` Git submodule) through HTTP endpoints.

## Endpoints

| Method | Path                   | Description        | Success status |
|--------|------------------------|--------------------|----------------|
| GET    | `/tasks-manager/tasks` | List all tasks     | 200            |
| POST   | `/tasks-manager/tasks` | Create a new task  | 201            |

### Create task — request body

```json
{
  "title": "Sample Task",
  "description": "This is a sample task with a description of at least 10 characters",
  "status": "IN_PROGRESS",
  "priority": "MEDIUM"
}
```

| Field         | Type   | Constraints                              | Default  |
|---------------|--------|------------------------------------------|----------|
| `title`       | string | min 5 chars                              | required |
| `description` | string | min 10 chars                             | required |
| `status`      | string | one of `TODO`, `IN_PROGRESS`, `DONE`     | `TODO`   |
| `priority`    | string | one of `URGENT`, `HIGH`, `MEDIUM`, `LOW` | `MEDIUM` |

## Module layout

| File                   | Responsibility                                                        |
|------------------------|-----------------------------------------------------------------------|
| `task_manager.py`      | API router: request model (`CreateTaskRequest`) and endpoint handlers |
| `init_task_manager.py` | Factory: builds a `TaskManager` from config (`create_task_manager()`) |
| `config.py`            | Loads `config.toml` via `tomllib` (`load_config()`)                   |
| `config.toml`          | Storage backend configuration                                         |
| `mapping.py`           | Maps API string values to `TaskStatus` / `TaskPriority` enums         |

## Configuration

`config.toml` selects the storage backend:

```toml
[storage]
type = "json"
path = "tasks.json"
```

- `type` — currently only `"json"` is supported.
- `path` — JSON file used by `JSONTaskStorage`. Relative paths resolve against the server working directory. The file is created (initialized with `[]`) on startup if missing or empty.

## How it fits together

1. On import, `task_manager.py` calls `create_task_manager()`.
2. `create_task_manager()` reads `config.toml` via `load_config()`.
3. For `type = "json"`, it ensures the parent directory exists, then instantiates `JSONTaskStorage(path)` and wraps it in a `TaskManager`.
4. Endpoints delegate to that shared `TaskManager` instance; request strings are converted to enums through `STATUS_MAPPING` / `PRIORITY_MAPPING`.

## Data model

Tasks are stored with the following fields (see `task_manager` package `models.py`):

```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "...",
  "status": "TODO",
  "priority": 2
}
```

Note: `priority` is serialized as its integer value (`URGENT=0`, `HIGH=1`, `MEDIUM=2`, `LOW=3`).
