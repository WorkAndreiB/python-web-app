from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)    

def test_generate_password():
    response = client.get("/password/generate-pass", params={"length": 16})
  
    assert response.status_code == 200

    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 16

def test_generate_password_default_length():
    response = client.get("/password/generate-pass")
  
    assert response.status_code == 202

    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 12 


@pytest.mark.parametrize("length", [7,129, -1, 0, "", "abc" ,None])
def test_generate_password_invalid_length(length):
    response = client.get("/password/generate-pass", params={"length": length})
    assert response.status_code == 422
