# Python Web App

Web app that provides access to independent Python projects through REST API. 

## Arhitecture
There are threee main components

+ [Frontend](/frontend/README.md): Web interface that communicates with backed through HTTP requests
+ [Backend](/backend/README.md): FastAPI app that exposes Python functionalities through REST endpoints
+ Python projects: Independend packages 

## Structure
```
python-web-app/
├── .devcontainer/
│   └── devcontainer.json
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── password_generator.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│
├── python/
│   └── password-generator/
│       ├── pyproject.toml
│       ├── src/
│       └── tests/
│
└── README.md
```

## Python projects integration

Python projects are maintained in a separate Git repository.

The repository is integrated into the web application using a Git submodule.

Python packages are installed after dev image is created

