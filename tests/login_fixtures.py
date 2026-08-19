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