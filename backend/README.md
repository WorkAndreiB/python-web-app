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

Manages tasks backed by JSON file storage. Router: [task_manager/](/backend/app/api/task_manager), mounted at prefix `/tasks-manager`. See the [Task Manager README](/backend/app/api/task_manager/README.md) for full details.

| Method | Path                   | Description       |
|--------|------------------------|-------------------|
| GET    | `/tasks-manager/tasks` | List all tasks    |
| POST   | `/tasks-manager/tasks` | Create a new task |

Storage backend is configured via [config.toml](/backend/app/api/task_manager/config.toml).

## Start local FastAPI server:
The devcontainer installs the local Python packages in editable mode, so source
changes are picked up when the server reloads. Initialize the Python submodule
before creating the devcontainer. Keep `backend/work_packages_dev.txt` in
sync with the production list in `backend/work_packages.txt` when adding
or removing packages. Reinstall after changing package metadata or dependencies.
Package paths are relative to the repository root. To install the production
packages locally, run `python -m pip install -r backend/work_packages.txt`
from the repository root after initializing the submodule.

1. ```uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload```

or

2. ```fastapi run /backend/app/main.y```

## Docker Containerization

Use [Dockerfile](/backend/Dockerfile) for local development

Use [Dockerfile.prod](/backend/Dockerfile.prod) to create the deployment image

Initialize the Python submodule before building the production image:
`git submodule update --init --recursive`. Build from the repository root with
`docker build -f backend/Dockerfile.prod -t deploy-image:latest .`.

The image contains:
+ Python runtime.
+ FastAPI and Uvicorn.
+ Backend application code.
+ The local packages listed in `backend/work_packages.txt`.


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