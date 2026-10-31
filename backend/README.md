# FastAPI backend

The backend uses FastAPI to expose Python functionality through HTTP endpoints.

+ Main application is responsible for createting the FastAPI instance and register routers
+ Each Python project can have it's own API router


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