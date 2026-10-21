from fastapi import FastAPI, Query
from password_generator import generate_password

app = FastAPI()


@app.get("/password")
def get_password(length: int = Query(default=12, ge=8, le=128)):
    password = generate_password(length)

    return {"password": password}