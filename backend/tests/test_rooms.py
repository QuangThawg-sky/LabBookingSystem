
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_staff_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "staff@labbooking.com",
            "password": "Staff@123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_get_rooms_requires_login():
    response = client.get("/rooms/")
    assert response.status_code == 401


def test_create_room_as_staff():
    token = get_staff_token()

    response = client.post(
        "/rooms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Phòng Pytest",
            "location": "Tầng 4 - Tòa nhà B",
            "capacity": 30,
            "description": "Phòng tạo bởi Pytest",
            "is_active": True
        }
    )

    assert response.status_code in [201, 409]


def test_get_room_not_found():
    token = get_staff_token()

    response = client.get(
        "/rooms/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
