# Beyond Main

[Beyond Main](https://beyond-main.andrei-baciu94.workers.dev/) is a personal portofolio & learning playground designed to introduce new skills through interactive applications. 

The project provides a web interface for interaction with different applications using different programming languages, frameworks and technologies. 

# Overview

Currently the application includes a password generator implemented in Python and exposed through a REST API. Users can select a password length, generate a random password, and copy the result to their clipboard.


## Arhitecture
There are threee main components

+ [Frontend](/frontend/README.md): Web interface that communicates with backed through HTTP requests
+ [Backend](/backend/README.md): FastAPI app that exposes Python functionalities through REST endpoints
+ Python projects: Independend packages 
+ The frontend and backend are hosted independently using Cloudflare Workers and Render.



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
|   ├── css
|   |   ├── style.css
|   ├── js
|   |   ├── api.js
|   |   └── main.js
|   └── index.html
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

## Features

The password generator is the first interactive application integrated into Beyond Main.

Features include:
+ Generate random passwords.
+ Configure password length between 8 and 128 characters.
+ Copy generated passwords to the clipboard.
+ Validate user input before sending requests.
+ Handle API errors and display feedback to the user.