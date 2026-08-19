from sqlalchemy import select

from app.schemas.user_schemas import UserChangePasswordSchema
from app.db.model import User
from app.authen.auth_passlib import verify_password


def test_change_password_success(
        client,
        login_user
):
    response = client.patch(
        "/users/password",
        json={
            "current_password": "strong password",
            "new_password": "password",
            "confirm_new_password": "password"
        },
        headers=login_user
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Пароль успішно змінено."

    old_password_response = client.post(
        "/auth/login",
        data={
            "username": "test_user",
            "password": "strong password"
        }
    )

    assert old_password_response.status_code == 401

    new_password_response = client.post(
        "/auth/login",
        data={
            "username": "test_user",
            "password": "password"
        }
    )

    assert new_password_response.status_code == 200
    assert "access_token" in new_password_response.json()


def test_change_password_success_service(
        user_service,
        db
):
    schema = UserChangePasswordSchema(
        current_password="strong password",
        new_password="password",
        confirm_new_password="password"
    )
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    result = user_service.change_password(db, user, schema)

    assert result["message"] == "Пароль успішно змінено."
    assert verify_password("password", user.password)
    assert not verify_password("strong password", user.password)


def test_change_password_wrong(
        client,
        login_user
):
    response = client.patch(
        "/users/password",
        json={
            "current_password": "stng password",
            "new_password": "password",
            "confirm_new_password": "password"
        },
        headers=login_user
    )

    assert response.status_code == 400
    assert "Невірний пароль" in response.json()["detail"]


def test_change_password_not_confirm(
        client,
        login_user
):
    response = client.patch(
        "/users/password",
        json={
            "current_password": "strong password",
            "new_password": "password",
            "confirm_new_password": "passrd"
        },
        headers=login_user
    )

    assert response.status_code == 422
    assert "Паролі не співпадають" in response.json()["detail"][0]["msg"]
