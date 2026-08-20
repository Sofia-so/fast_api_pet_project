from sqlalchemy import select

from app.db.model import User
from app.db.model_enum import UserRole


def test_get_list_employees_success(
        client,
        login_admin,
        db
):
    response = client.get(
        "/admin/employees",
        headers=login_admin
    )

    employees = db.scalars(
        select(User).where(User.role == "employee")
    ).all()
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == len(employees)
    assert any(
        employee["username"] == "test_employee"
        for employee in response_json
    )

    assert all(
        employee["role"] == "employee"
        for employee in response_json
    )


def test_get_list_employee_service_success(
        admin_service,
        db
):
    result = admin_service.get_list_employees(db)

    employees = db.scalars(
        select(User).where(User.role == "employee")
    ).all()

    assert len(result) == len(employees)
    assert any(
        employee.username == "test_employee"
        for employee in result
    )
    assert all(
        employee.role == UserRole.EMPLOYEE
        for employee in result
    )


def test_get_list_employees_without_success(
        client,
        login_user
):
    response = client.get(
        "/admin/employees",
        headers=login_user
    )

    assert response.status_code == 403
