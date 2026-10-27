from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import password_generator
from .api import books


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(
    router=password_generator.pass_generator_router,
    prefix="/password",
    tags=["Password Generator"]
)

app.include_router(
    router=books.router,
    prefix="/books",
    tags=["Books"]
)