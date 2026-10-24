from fastapi import FastAPI
from .api import password_generator

app = FastAPI()

app.include_router(
    router=password_generator.pass_generator_router,
    prefix="/password",
    tags=["Password Generator"]
)