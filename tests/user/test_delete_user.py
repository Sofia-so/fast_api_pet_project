from sqlalchemy import select

from app.db.model import User


def test_delete_user_success(
        client,
        login_user,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    response = client.delete(
        "/users/me",
        headers=login_user
    )

    deleted_user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert response.status_code == 200
    assert deleted_user is None
    assert response.json()["message"] == "Акаунт успішно видалено"


def test_delete_user_service_success(
        user_service,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    result = user_service.delete_user(db, user)

    deleted_user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert deleted_user is None
    assert result["message"] == "Акаунт успішно видалено"


def test_delete_user_with_order(
        client,
        login_user,
        db,
        create_order
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    response = client.delete(
        "/users/me",
        headers=login_user
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Неможна видалити акаунт, "
               "оскільки на ньому є активні замовлення")


def test_delete_user_wrong_token(client):

    response = client.delete(
        "/users/me",
        headers={
            "Authorization": f"Bearer token"
        }
    )

    assert response.status_code == 401
