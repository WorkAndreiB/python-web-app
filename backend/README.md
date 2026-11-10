# FastAPI backend

The backend uses FastAPI to expose Python functionality through HTTP endpoints.

+ Main application is responsible for createting the FastAPI instance and register routers
+ Each Python project can have it's own API router

## APIs

### Password Generator

Generates random passwords. Router: [password_generator.py](/backend/app/api/password_generator.py), mounted at prefix `/password`.

| Method | Path                      | Description              |
|--------|---------------------------|--------------------------|
| GET    | `/password/generate-pass` | Generate a random password |

Query parameters:

| Parameter | Type | Constraints      | Default |
|-----------|------|------------------|---------|
| `length`  | int  | between 8 and 128 | 12      |

Response:

```json
{"password": "aB3$xY9..."}
```

### Task Manager

Manages tasks backed by JSON file storage. Router: [task_manager/](/backend/app/api/task_manager), mounted at prefix `/tasks`. See the [Task Manager README](/backend/app/api/task_manager/README.md) for full details.

| Method | Path     | Description       |
|--------|----------|-------------------|
| GET    | `/tasks` | List all tasks    |
| POST   | `/tasks` | Create a new task |

Storage backend is configured via [config.toml](/backend/app/api/task_manager/config.toml).

## Start local FastAPI server:
1. ```uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload```

or

2. ```fastapi run /backend/app/main.y```

## Docker Containerization

Use [Dockerfile](/backend/Dockerfile) for local development

Use [Dockerfile.prod](/backend/Dockerfile.prod) to create the deployment image

The image contains:
+ Python runtime.
+ FastAPI and Uvicorn.
+ Backend application code.
+ The installable password-generator package.


## Testing

Test workflow runs automatically when relevant changes are introduced through pull requests or pushed to the main branch.

Workflow:
+ Checks out the repository.
+ Initializes the required Python Git submodule.
+ Installs Python dependencies.
+ Runs automated tests using pytest.


## Deployment

Hosted on Render.

Render builds the backend's production Docker image and deploys the resulting container.