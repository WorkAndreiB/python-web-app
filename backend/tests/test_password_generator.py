from backend.app.api import password_generator
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

pass_generator_app = FastAPI()
pass_generator_app.include_router(
    router=password_generator.pass_generator_router,
    prefix="/password",
    tags=["Password Generator"]
)

pass_generator_client = TestClient(pass_generator_app)    

def test_generate_password():
    response = pass_generator_client.get("/password/generate-pass", params={"length": 16})
  
    assert response.status_code == 200

    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 16

def test_generate_password_default_length():
    response = pass_generator_client.get("/password/generate-pass")
  
    assert response.status_code == 200

    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 12 


@pytest.mark.parametrize("length", [7,129, -1, 0, "", "abc" ,None])
def test_generate_password_invalid_length(length):
    response = pass_generator_client.get("/password/generate-pass", params={"length": length})
    assert response.status_code == 422
