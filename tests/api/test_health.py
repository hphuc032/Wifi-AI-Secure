
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "Wifi-AI Secure"
    assert response.json()["version"] == "0.1.0"
    assert response.json()["status"] == "running"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "wifi-ai-secure-api",
    }


def test_unknown_endpoint():
    response = client.get("/nonexistent")

    assert response.status_code == 404


def test_openapi_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
