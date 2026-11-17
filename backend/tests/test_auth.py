
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["project"] == "Lab Booking System"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_success():
    response = client.post(
        "/auth/login",
        json={
            "email": "student@labbooking.com",
            "password": "Student@123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post(
        "/auth/login",
        json={
            "email": "student@labbooking.com",
            "password": "WrongPassword123"
        }
    )
    assert response.status_code == 401
