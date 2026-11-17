
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


def test_get_equipment_requires_login():
    response = client.get("/equipment/")
    assert response.status_code == 401


def test_get_equipment_list():
    token = get_staff_token()

    response = client.get(
        "/equipment/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_equipment():
    token = get_staff_token()

    response = client.get(
        "/equipment/?search=may",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_filter_equipment_by_status():
    token = get_staff_token()

    response = client.get(
        "/equipment/?status=available",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_equipment_pagination():
    token = get_staff_token()

    response = client.get(
        "/equipment/?skip=0&limit=2",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) <= 2


def test_equipment_not_found():
    token = get_staff_token()

    response = client.get(
        "/equipment/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

