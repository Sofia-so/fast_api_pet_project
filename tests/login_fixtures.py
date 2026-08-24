import pytest


@pytest.fixture(scope="function")
def login_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_user",
            "password": "strong password"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def login_admin(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_admin",
            "password": "strong password"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def login_employee(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_employee",
            "password": "strong password"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
