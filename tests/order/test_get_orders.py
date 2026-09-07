from sqlalchemy import select
from decimal import Decimal

from app.db.model import (
    Order,
    User
)
from app.db.model_enum import UserRole


def test_get_orders_admin(
        client,
        create_order,
        login_admin,
        db
):
    response = client.get(
        "/orders/",
        headers=login_admin
    )

    orders = db.scalars(
        select(Order).order_by(Order.created_at.desc())
    ).all()

    response_json = response.json()

    assert response.status_code == 200
    assert len(orders) == len(response_json)
    for order, response_order in zip(orders, response_json):
        assert (response_order["customer_first_name"]
                == order.customer_first_name)
        assert (response_order["customer_last_name"]
                == order.customer_last_name)
        assert (response_order["customer_phone"]
                == order.customer_phone)
        assert (response_order["delivery_method"]
                == order.delivery_method.value)
        assert response_order["number"] == order.number
        assert response_order["status"] == order.status.value
        assert (Decimal(response_order["total_price"])
                == order.total_price)
        assert (response_order["created_at"]
                == order.created_at.isoformat())
        assert response_order["user_id"] == order.user_id


def test_get_orders_user(
        client,
        create_order,
        login_user,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )
    user_id = user.id

    assert user is not None
    assert user.role.value == "client"

    response = client.get(
        "/orders/",
        headers=login_user
    )

    orders = db.scalars(
        select(Order).where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    ).all()

    response_json = response.json()

    assert response.status_code == 200

    for response_order in response_json:
        assert response_order["user_id"] == user_id

    assert len(orders) == len(response_json)
    for order, response_order in zip(orders, response_json):
        assert (response_order["customer_first_name"]
                == order.customer_first_name)
        assert (response_order["customer_last_name"]
                == order.customer_last_name)
        assert (response_order["customer_phone"]
                == order.customer_phone)
        assert (response_order["delivery_method"]
                == order.delivery_method.value)
        assert response_order["number"] == order.number
        assert response_order["status"] == order.status.value
        assert (Decimal(response_order["total_price"])
                == order.total_price)
        assert (response_order["created_at"]
                == order.created_at.isoformat())
        assert response_order["user_id"] == order.user_id


def test_get_orders_service_admin(
        order_service,
        create_order,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_admin")
    )

    assert user is not None

    orders = db.scalars(
        select(Order).where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    ).all()

    result = order_service.get_orders(
        db,
        user
    )

    for order, result_order in zip(orders, result):
        assert (result_order.customer_first_name
                == order.customer_first_name)
        assert (result_order.customer_last_name
                == order.customer_last_name)
        assert (result_order.customer_phone
                == order.customer_phone)
        assert (result_order.delivery_method
                == order.delivery_method)
        assert result_order.number == order.number
        assert result_order.status == order.status
        assert result_order.total_price == order.total_price
        assert (result_order.created_at
                == order.created_at)
        assert result_order.user_id == order.user_id


def test_get_orders_service_user(
        order_service,
        create_order,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None
    assert user.role == UserRole.CLIENT

    user_id = user.id

    orders = db.scalars(
        select(Order).where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    ).all()

    result = order_service.get_orders(
        db,
        user
    )

    for result_order in result:
        assert result_order.user_id == user_id

    for order, result_order in zip(orders, result):
        assert (result_order.customer_first_name
                == order.customer_first_name)
        assert (result_order.customer_last_name
                == order.customer_last_name)
        assert (result_order.customer_phone
                == order.customer_phone)
        assert (result_order.delivery_method
                == order.delivery_method)
        assert result_order.number == order.number
        assert result_order.status == order.status
        assert result_order.total_price == order.total_price
        assert (result_order.created_at
                == order.created_at)
        assert result_order.user_id == order.user_id
