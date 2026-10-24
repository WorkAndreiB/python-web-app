from fastapi import APIRouter, Query
from password_generator import generate_password

pass_generator_router = APIRouter()

@pass_generator_router.get("/generate-pass")
def get_password(length: int = Query(default=12, ge=8, le=128)):
    password = generate_password(length)

    return {"password": password}