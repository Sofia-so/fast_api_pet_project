from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import Order
from app.schemas.order_schemas import OrderChangeStatusSchema
from app.db.model_enum import OrderStatus


def test_change_order_status(
        client,
        login_employee,
        create_order,
        db
):
    number = "ORD-001"

    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status.value == "pending"

    response = client.patch(
        f"/orders/{number}/status",
        json={"status": "processing"},
        headers=login_employee
    )

    db.expire_all()

    assert response.status_code == 200
    assert response.json()["status"] == "processing"


def test_change_order_status_bad_request(
        client,
        login_employee,
        create_order,
        db
):
    number = "ORD-001"

    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status.value == "pending"

    response = client.patch(
        f"/orders/{number}/status",
        json={"status": "pending"},
        headers=login_employee
    )

    assert response.status_code == 400
    assert (response.json()["detail"]
            == "Замовлення вже має цей статус.")


def test_change_order_status_conflict(
        client,
        login_employee,
        create_order,
        db
):
    number = "ORD-001"

    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status.value == "pending"

    response = client.patch(
        f"/orders/{number}/status",
        json={"status": "shipped"},
        headers=login_employee
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Не можна змінити статус з 'pending' на 'shipped'.")


def test_change_order_status_forbidden(
        client,
        login_user,
        create_order,
        db
):
    number = "ORD-001"

    response = client.patch(
        f"/orders/{number}/status",
        json={"status": "processing"},
        headers=login_user
    )

    assert response.status_code == 403
    assert (response.json()["detail"]
            == "Недостатньо прав доступу")


def test_change_order_status_service(
        order_service,
        create_order,
        db
):
    number = create_order.number
    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status == OrderStatus.PENDING

    schema = OrderChangeStatusSchema(
        status=OrderStatus.PROCESSING
    )

    result = order_service.change_order_status(
        db,
        number,
        schema
    )

    db.expire_all()

    assert result.status == OrderStatus.PROCESSING


def test_change_order_status_service_bad_request(
        order_service,
        create_order,
        db
):
    number = create_order.number
    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status == OrderStatus.PENDING

    schema = OrderChangeStatusSchema(
        status=OrderStatus.PENDING
    )

    with pytest.raises(HTTPException) as exc_info:
        order_service.change_order_status(
            db,
            number,
            schema
        )

    assert exc_info.value.status_code == 400
    assert (exc_info.value.detail
            == "Замовлення вже має цей статус.")


def test_change_order_status_service_conflict(
        order_service,
        create_order,
        db
):
    number = create_order.number
    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None
    assert order.status == OrderStatus.PENDING

    schema = OrderChangeStatusSchema(
        status=OrderStatus.SHIPPED
    )

    with pytest.raises(HTTPException) as exc_info:
        order_service.change_order_status(
            db,
            number,
            schema
        )

    assert exc_info.value.status_code == 409
    assert (exc_info.value.detail
            == "Не можна змінити статус з 'pending' на 'shipped'.")
