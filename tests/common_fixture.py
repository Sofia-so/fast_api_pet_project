import pytest
from sqlalchemy import delete

from app.db.model import User
from app.db.model_enum import UserRole
from app.authen.auth_passlib import hash_password


@pytest.fixture(scope="function", autouse=True)
def create_users(db):

    password = "strong password"

    test_user = User(
        first_name="test_user",
        last_name="test_user",
        username="test_user",
        email="email_user@test.com",
        password=hash_password(password),
        role=UserRole.CLIENT
    )

    test_employee = User(
        first_name="test_employee",
        last_name="test_employee",
        username="test_employee",
        email="email_employee@test.com",
        password=hash_password(password),
        role=UserRole.EMPLOYEE
    )

    test_admin = User(
        first_name="test_admin",
        last_name="test_admin",
        username="test_admin",
        email="email_admin@test.com",
        password=hash_password(password),
        role=UserRole.ADMIN
    )

    db.add_all([
        test_user,
        test_employee,
        test_admin
    ])
    db.commit()

    yield

    db.execute(delete(User))
    db.commit()


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
