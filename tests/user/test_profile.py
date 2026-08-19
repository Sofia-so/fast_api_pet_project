from sqlalchemy import select

from app.db.model import User
from app.db.model_enum import UserRole


def test_profile(
        client,
        login_user,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    response = client.get(
        "users/me",
        headers=login_user
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["first_name"] == user.first_name
    assert response_json["first_name"] == "test_user"
    assert response_json["last_name"] == user.last_name
    assert response_json["username"] == user.username
    assert response_json["email"] == user.email
    assert response_json["role"] == "client"
    assert user.role == UserRole.CLIENT


def test_profile_service(
        user_service,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    result = user_service.profile(user)

    assert result.first_name == user.first_name
    assert result.last_name == user.last_name
    assert result.username == user.username
    assert result.email == user.email
    assert result.role == user.role
