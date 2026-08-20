from sqlalchemy import select

from app.db.model import User
from app.authen.auth_passlib import verify_password
from app.db.model_enum import UserRole
from app.schemas.user_schemas import UserCreateSchema


def test_create_employee_success(
        client,
        login_admin,
        db
):
    response = client.post(
        "/admin/employee",
        json={
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "test@ttt.com",
            "password": "password",
            "confirm_password": "password"
        },
        headers=login_admin
    )

    response_json = response.json()
    employee = db.scalar(
        select(User).where(User.username=="test")
    )

    assert employee is not None
    assert response.status_code == 201
    assert response_json["first_name"] == employee.first_name
    assert response_json["last_name"] == employee.last_name
    assert response_json["username"] == employee.username
    assert response_json["email"] == employee.email
    assert verify_password("password", employee.password)
    assert employee.role == UserRole.EMPLOYEE
    assert response_json["role"] == "employee"


def test_create_employee_service_success(
        admin_service,
        db
):
    user = UserCreateSchema(
        first_name="test",
        last_name="test",
        username="test",
        email="test@ttt.com",
        password="password",
        confirm_password="password"
    )

    result = admin_service.create_employee(db, user)

    employee = db.scalar(
        select(User).where(User.username=="test")
    )

    assert employee is not None
    assert result.first_name == employee.first_name
    assert result.last_name == employee.last_name
    assert result.username == employee.username
    assert result.email == employee.email
    assert verify_password("password", employee.password)
    assert employee.role == UserRole.EMPLOYEE
    assert result.role == UserRole.EMPLOYEE


def test_create_employee_without_access(
        client,
        login_user
):
    response = client.post(
        "/admin/employee",
        json={
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "test@ttt.com",
            "password": "password",
            "confirm_password": "password"
        },
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"


def test_create_employee_duplicate_username(
        client,
        login_admin,
        db
):
    response = client.post(
        "/admin/employee",
        json={
            "first_name": "test",
            "last_name": "test",
            "username": "test_employee",
            "email": "test@ttt.com",
            "password": "password",
            "confirm_password": "password"
        },
        headers=login_admin
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")


def test_create_employee_duplicate_email(
        client,
        login_admin,
        db
):
    response = client.post(
        "/admin/employee",
        json={
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "email_employee@test.com",
            "password": "password",
            "confirm_password": "password"
        },
        headers=login_admin
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Користувач з таким ім'ям або email вже існує.")

def test_create_employee_not_match_password(
        client,
        login_admin,
        db
):
    response = client.post(
        "/admin/employee",
        json={
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "email_employee77@test.com",
            "password": "password",
            "confirm_password": "pass"
        },
        headers=login_admin
    )

    assert response.status_code == 422
    assert "Паролі не співпадають" in response.json()["detail"][0]["msg"]
