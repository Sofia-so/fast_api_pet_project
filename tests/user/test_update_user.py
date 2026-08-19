from sqlalchemy import select

from app.db.model import User
from app.schemas.user_schemas import UserUpdateSchema


def test_update_user_success(
        client,
        db,
        login_user
):
    user = db.scalar(
        select(User).where(User.username=="test_user")
    )

    assert user is not None

    response = client.patch(
        "/users/me",
        json={
            "username": "user_test"
        },
        headers=login_user
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["message"] == "Дані користувача успішно оновлено."

    updated_user = db.scalar(
        select(User).where(User.username=="user_test")
    )

    assert updated_user is not None
    assert updated_user.email == "email_user@test.com"


def test_update_user_service_success(
        user_service,
        db
):
    user = db.scalar(
        select(User).where(User.username=="test_user")
    )
    schema = UserUpdateSchema(
        username="user_test"
    )

    assert user is not None

    result = user_service.update_user(
        db,
        user,
        schema
    )

    assert (result["message"]
            == "Дані користувача успішно оновлено.")
    assert user.username == "user_test"


def test_update_user_conflict_name(
        client,
        login_user,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_employee")
    )
    assert user is not None

    response = client.patch(
        "/users/me",
        json={
            "username": "test_employee"
        },
        headers=login_user
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")


def test_update_user_conflict_email(
        client,
        login_user,
        db
):
    user = db.scalar(
        select(User).where(User.email == "email_employee@test.com")
    )
    assert user is not None

    response = client.patch(
        "/users/me",
        json={
            "email": "email_employee@test.com"
        },
        headers=login_user
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")
