from sqlalchemy import select
from decimal import Decimal
import pytest
from fastapi import HTTPException

from app.db.model import (
    Product,
    Order,
    OrderItem,
    User
)
from app.schemas.order_schemas import (
    OrderCreateSchema,
    OrderItemSchema
)
from app.db.model_enum import (
    DeliveryMethod,
    OrderStatus,
    ProductStatus
)


def test_create_order_success(
        client,
        login_user,
        db
):
    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product1 is not None

    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert product2 is not None

    response = client.post(
        "/orders/",
        json={
            "customer_first_name": "customer_first_name",
            "customer_last_name": "customer_last_name",
            "customer_phone": "+380000000000",
            "delivery_method": "pickup",
            "items": [
                {
                    "product_id": product1.id,
                    "quantity": 6
                },
                {
                    "product_id": product2.id,
                    "quantity": 4
                }
            ]
        },
        headers=login_user
    )

    assert response.status_code == 201

    response_json = response.json()
    order_id = response_json["id"]
    total_price = (6 * product1.price) + (4 * product2.price)

    db.expire_all()

    order = db.get(Order, order_id)

    assert order is not None

    order_items = db.scalars(
        select(OrderItem).where(OrderItem.order_id == order.id)
    ).all()

    updated_product1 = db.get(Product, product1.id)
    updated_product2 = db.get(Product, product2.id)

    expected = sorted(
        (
            item.product_id,
            item.product_name,
            item.quantity,
            item.price
        )
        for item in order_items
    )
    actual = sorted(
        (
            item["product_id"],
            item["product_name"],
            item["quantity"],
            Decimal(item["price"])
        )
        for item in response_json["items"]
    )

    assert (response_json["customer_first_name"]
            == order.customer_first_name)
    assert (response_json["customer_last_name"]
            == order.customer_last_name)
    assert (response_json["customer_phone"]
            == order.customer_phone)
    assert (response_json["delivery_method"]
            == order.delivery_method.value)
    assert response_json["number"] == order.number
    assert response_json["status"] == "pending"
    assert response_json["status"] == order.status.value
    assert (Decimal(response_json["total_price"])
            == total_price)
    assert (response_json["created_at"]
            == order.created_at.isoformat())
    assert response_json["user_id"] == order.user_id

    assert updated_product1.quantity == 7
    assert updated_product2.quantity == 0
    assert updated_product1.status.value == "available"
    assert updated_product2.status.value == "out_of_stock"

    assert expected == actual


def test_create_order_service_success(
        order_service,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product1 is not None

    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert product2 is not None

    schema = OrderCreateSchema(
        customer_first_name = "customer_first_name",
        customer_last_name = "customer_last_name",
        customer_phone = "+380000000000",
        delivery_method = DeliveryMethod.PICKUP,
        items = [
            OrderItemSchema(
                product_id=product1.id,
                quantity=6,
            ),
            OrderItemSchema(
                product_id=product2.id,
                quantity=4,
            ),
        ]
    )

    result = order_service.create_order(
        db,
        user,
        schema
    )

    order_id = result.id
    total_price = (6 * product1.price) + (4 * product2.price)

    db.expire_all()

    order = db.get(Order, order_id)

    assert order is not None

    order_items = db.scalars(
        select(OrderItem).where(OrderItem.order_id == order.id)
    ).all()

    updated_product1 = db.get(Product, product1.id)
    updated_product2 = db.get(Product, product2.id)

    expected = sorted(
        (
            item.product_id,
            item.product_name,
            item.quantity,
            item.price
        )
        for item in order_items
    )
    actual = sorted(
        (
            item.product_id,
            item.product_name,
            item.quantity,
            item.price
        )
        for item in result.items
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
    assert result.status == OrderStatus.PENDING
    assert result.status == order.status
    assert (result.total_price
            == total_price)
    assert (result.created_at
            == order.created_at)
    assert result.user_id == order.user_id

    assert updated_product1.quantity == 7
    assert updated_product2.quantity == 0
    assert (updated_product1.status
            == ProductStatus.AVAILABLE)
    assert (updated_product2.status
            == ProductStatus.OUT_OF_STOCK)

    assert expected == actual


def test_create_order_insufficient_stock(
        client,
        login_user,
        db
):
    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product1 is not None

    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert product2 is not None

    response = client.post(
        "/orders/",
        json={
            "customer_first_name": "customer_first_name",
            "customer_last_name": "customer_last_name",
            "customer_phone": "+380000000000",
            "delivery_method": "pickup",
            "items": [
                {
                    "product_id": product1.id,
                    "quantity": 10000
                },
                {
                    "product_id": product2.id,
                    "quantity": 4
                }
            ]
        },
        headers=login_user
    )

    assert response.status_code == 400
    assert (response.json()["detail"]
            == f"Недостатньо товару '{product1.name}' на складі. "
               f"Доступна кількість товару {product1.quantity}")


def test_create_order_service_insufficient_stock(
        order_service,
        db
):
    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product1 is not None

    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert product2 is not None

    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    schema = OrderCreateSchema(
        customer_first_name="customer_first_name",
        customer_last_name="customer_last_name",
        customer_phone="+380000000000",
        delivery_method=DeliveryMethod.PICKUP,
        items=[
            OrderItemSchema(
                product_id=product1.id,
                quantity=10000,
            ),
            OrderItemSchema(
                product_id=product2.id,
                quantity=4,
            ),
        ]
    )

    with pytest.raises(HTTPException) as exc_info:
        order_service.create_order(
            db,
            user,
            schema
        )
    assert exc_info.value.status_code == 400
    assert (exc_info.value.detail
            == f"Недостатньо товару '{product1.name}' на складі. "
               f"Доступна кількість товару {product1.quantity}")


def test_create_order_without_authen(
        client,
        db
):
    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product1 is not None

    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert product2 is not None

    response = client.post(
        "/orders/",
        json={
            "customer_first_name": "customer_first_name",
            "customer_last_name": "customer_last_name",
            "customer_phone": "+380000000000",
            "delivery_method": "pickup",
            "items": [
                {
                    "product_id": product1.id,
                    "quantity": 6
                },
                {
                    "product_id": product2.id,
                    "quantity": 4
                }
            ]
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
