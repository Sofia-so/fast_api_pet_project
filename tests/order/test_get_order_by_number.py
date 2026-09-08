from sqlalchemy import select
from decimal import Decimal
import pytest
from fastapi import HTTPException

from app.db.model import Order


def test_get_order_by_number(
        client,
        login_admin,
        create_order,
        db
):
    number = "ORD-001"

    response = client.get(
        f"/orders/{number}",
        headers=login_admin
    )

    response_json = response.json()

    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None

    assert response.status_code == 200

    assert (response_json["customer_first_name"]
            == order.customer_first_name)
    assert (response_json["customer_last_name"]
            == order.customer_last_name)
    assert (response_json["customer_phone"]
            == order.customer_phone)
    assert (response_json["delivery_method"]
            == order.delivery_method.value)
    assert response_json["number"] == order.number
    assert response_json["status"] == order.status.value
    assert (Decimal(response_json["total_price"])
            == order.total_price)
    assert (response_json["created_at"]
            == order.created_at.isoformat())
    assert response_json["user_id"] == order.user_id


def test_get_order_by_number_not_found(
        client,
        login_admin,
        db
):
    response = client.get(
        "/orders/ORD",
        headers=login_admin
    )

    assert response.status_code == 404
    assert (response.json()["detail"]
            == "Замовлення не знайдено.")


def test_get_order_by_number_forbidden(
        client,
        login_user,
        db
):
    response = client.get(
        "/orders/ORD",
        headers=login_user
    )

    assert response.status_code == 403
    assert (response.json()["detail"]
            == "Недостатньо прав доступу")


def test_get_order_by_number_service(
        order_service,
        create_order,
        db
):
    number = "ORD-001"

    order = db.scalar(
        select(Order).where(Order.number == number)
    )

    assert order is not None

    result = order_service.get_order_by_number(
        db,
        number
    )

    assert (result.customer_first_name
            == order.customer_first_name)
    assert (result.customer_last_name
            == order.customer_last_name)
    assert (result.customer_phone
            == order.customer_phone)
    assert (result.delivery_method
            == order.delivery_method)
    assert result.number == order.number
    assert result.status == order.status
    assert (result.total_price
            == order.total_price)
    assert (result.created_at
            == order.created_at)
    assert result.user_id == order.user_id


def test_get_order_by_number_service_not_found(
        order_service,
        db
):
    number = "ORD"

    with pytest.raises(HTTPException) as exc_info:
        order_service.get_order_by_number(
            db,
            number
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Замовлення не знайдено."
