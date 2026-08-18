from sqlalchemy import select

from app.db.model import BlacklistedToken


def test_logout(
        login_user,
        client,
        db
):
    response = client.post(
        "/auth/logout",
        headers=login_user
    )

    token = login_user["Authorization"].replace("Bearer ", "")

    blacklisted_token = db.scalar(
        select(BlacklistedToken).where(
            BlacklistedToken.token == token
        )
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Успішний вихід із системи."
    assert blacklisted_token is not None


def test_logout_service(auth_service, db):
    token = "test_token"

    result = auth_service.logout(db, token)

    assert result.message == "Успішний вихід із системи."

    blacklisted = db.scalar(
        select(BlacklistedToken).where(
            BlacklistedToken.token == token
        )
    )

    assert blacklisted is not None
    assert blacklisted.token == token
