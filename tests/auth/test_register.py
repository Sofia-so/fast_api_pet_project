from sqlalchemy import select

from app.db.model import User
from app.schemas.user_schemas import UserCreateSchema
from app.authen.auth_passlib import verify_password
from app.db.model_enum import UserRole


def test_register_success(
        client,
        db
):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "test_user",
            "last_name": "test_user",
            "username": "test_test_user",
            "email": "test_user@email.com",
            "password": "password",
            "confirm_password": "password"
        }
    )

    data = response.json()
    user = db.scalar(
        select(User).where(User.username=="test_test_user")
    )

    assert response.status_code == 201
    assert data["username"] == "test_test_user"
    assert user is not None
    assert user.email == "test_user@email.com"


def test_register_success_service(auth_service, db):
    user = UserCreateSchema(
        first_name="test",
        last_name="test",
        username="test_user344",
        email="test@test.com",
        password="password",
        confirm_password="password"
    )

    result = auth_service.register(db, user)
    saved_user = db.scalar(
        select(User).where(User.username == "test_user344")
    )

    assert result is not None
    assert result.username == "test_user344"
    assert result.email == "test@test.com"
    assert result.first_name == "test"
    assert result.last_name == "test"
    assert verify_password("password", result.password)
    assert result.role == UserRole.CLIENT
    assert saved_user is not None
    assert saved_user.email == "test@test.com"


def test_duplicate_username(client, db):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "test_user",
            "last_name": "test_user",
            "username": "test_user",
            "email": "test_user@email.com",
            "password": "password",
            "confirm_password": "password"
        }
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")


def test_register_duplicate_email(
        client,
        db
):

    response = client.post(
        "/auth/register",
        json={
            "first_name": "test_user",
            "last_name": "test_user",
            "username": "test_client",
            "email": "email_user@test.com",
            "password": "password",
            "confirm_password": "password"
        }
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")


def test_register_passwords_d_not_match(
        client,
        db
):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "test_user",
            "last_name": "test_user",
            "username": "test_user_test2",
            "email": "testuser44@email.com",
            "password": "password",
            "confirm_password": "password44"
        }
    )
    response_json = response.json()
    assert response.status_code == 422
    assert "Паролі не співпадають" in response_json["detail"][0]["msg"]
