from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import User


def test_delete_employee_success(
        client,
        login_admin,
        db
):
    employee = db.scalar(
        select(User).where(User.username == "test_employee")
    )

    assert employee is not None

    user_id = employee.id
    response = client.delete(
        f"/admin/employee/{user_id}",
        headers=login_admin
    )

    deleted_employee = db.scalar(
        select(User).where(User.id == user_id)
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Працівника успішно видалено"
    assert deleted_employee is None


def test_delete_employee_service_success(
        admin_service,
        db
):
    employee = db.scalar(
        select(User).where(User.username == "test_employee")
    )

    assert employee is not None

    result = admin_service.delete_employee(db, employee)

    deleted_employee = db.scalar(
        select(User).where(User.username == "test_employee")
    )

    assert deleted_employee is None
    assert result["message"] == "Працівника успішно видалено"


def test_delete_employee_with_role_user(
        client,
        login_admin,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    user_id = user.id
    response = client.delete(
        f"/admin/employee/{user_id}",
        headers=login_admin
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Можна видаляти лише працівників."


def test_delete_employee_service_with_role_user(
        admin_service,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    with pytest.raises(HTTPException) as exc_info:
        admin_service.delete_employee(db, user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Можна видаляти лише працівників."


def test_delete_employee_without_access_role(
        client,
        login_user,
        db
):
    employee = db.scalar(
        select(User).where(User.username == "test_employee")
    )

    assert employee is not None

    user_id = employee.id
    response = client.delete(
        f"/admin/employee/{user_id}",
        headers=login_user
    )

    assert response.status_code == 403
