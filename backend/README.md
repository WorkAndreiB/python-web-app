# FastAPI backend

The backend uses FastAPI to expose Python functionality through HTTP endpoints.

+ Main application is responsible for createting the FastAPI instance and register routers
+ Each Python project can have it's own API router

## Available API Endpoints
Endpoint

```GET /password/generate-pass```

## Start FastAPI server:
1. ```uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload```

2. ```fastapi run /backend/app/main.y```

