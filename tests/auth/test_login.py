from fastapi.security import OAuth2PasswordRequestForm
import pytest
from fastapi import HTTPException


def test_login_right(client, db):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_user",
            "password": "strong password"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_username(client, db):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_usr",
            "password": "strong password"
        }
    )

    assert response.status_code == 401
    assert "Невірний логін або пароль" in response.json()["detail"]


def test_login_wrong_password(client, db):
    response = client.post(
        "auth/login",
        data={
            "username": "test_user",
            "password": "strong paord"
        }
    )

    assert response.status_code == 401
    assert "Невірний логін або пароль" in response.json()["detail"]


def test_login_success_service(auth_service, db):
    form_data = OAuth2PasswordRequestForm(
        username="test_user",
        password="strong password"
    )

    result = auth_service.login(db, form_data)

    assert result is not None
    assert "access_token" in result
    assert result["access_token"]
    assert result["token_type"] == "bearer"


def test_login_wrong_password_service(
        auth_service,
        db
):
    form_data = OAuth2PasswordRequestForm(
        username="test_user",
        password="strong pord"
    )

    with pytest.raises(HTTPException) as exc_info:
        auth_service.login(db, form_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Невірний логін або пароль"


def test_login_invalid_request(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test_user"
        }
    )

    assert response.status_code == 422
