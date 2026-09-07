from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import (
    Product,
    Order,
    User
)
from app.db.model_enum import (
    OrderStatus,
    UserRole
)
from app.authen.auth_passlib import hash_password


def test_cancel_order_success(
        client,
        login_user,
        create_order,
        db
):
    order_id = create_order.id

    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )
    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )
    initial_product1_quantity = product1.quantity
    initial_product2_quantity = product2.quantity
    product1_item = next(
        item for item in create_order.items
        if item.product_id == product1.id
    )
    product2_item = next(
        item for item in create_order.items
        if item.product_id == product2.id
    )

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=login_user
    )

    db.expire_all()

    order = db.get(Order, order_id)

    assert order is not None

    updated_product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )
    updated_product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )


    assert response.status_code == 200
    assert order.status.value == "cancelled"
    assert updated_product1.quantity == (
            initial_product1_quantity + product1_item.quantity
    )
    assert updated_product2.quantity == (
            initial_product2_quantity + product2_item.quantity
    )


def test_cancel_order_service_success(
        order_service,
        create_order,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    assert user is not None

    order_id = create_order.id
    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )
    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )
    initial_product1_quantity = product1.quantity
    initial_product2_quantity = product2.quantity
    product1_item = next(
        item for item in create_order.items
        if item.product_id == product1.id
    )
    product2_item = next(
        item for item in create_order.items
        if item.product_id == product2.id
    )

    order_service.cancel_order(
        db,
        user,
        order_id
    )

    db.expire_all()

    order = db.get(Order, order_id)

    updated_product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )
    updated_product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    assert order is not None
    assert order.status == OrderStatus.CANCELLED
    assert updated_product1.quantity == (
            initial_product1_quantity + product1_item.quantity
    )
    assert updated_product2.quantity == (
            initial_product2_quantity + product2_item.quantity
    )


def test_cancel_order_forbidden(
        client,
        create_order,
        db
):
    register_response = client.post(
        "/auth/register",
        json={
            "first_name": "test_user",
            "last_name": "test_user",
            "username": "test_user_test",
            "email": "testuser44@email.com",
            "password": "password",
            "confirm_password": "password"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": "test_user_test",
            "password": "password"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    order_id = create_order.id

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403
    assert (response.json()["detail"]
            == "Ви можете скасувати лише власні замовлення.")


def test_cancel_order_service_forbidden(
        order_service,
        create_order,
        db
):
    password = "password"

    user = User(
        first_name="test_user",
        last_name="test_user",
        username="test_user_test",
        email="email_user@test_test.com",
        password=hash_password(password),
        role=UserRole.CLIENT
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user is not None

    order_id = create_order.id

    with pytest.raises(HTTPException) as exc_info:
        order_service.cancel_order(
            db,
            user,
            order_id
        )

    assert exc_info.value.status_code == 403
    assert (exc_info.value.detail
            == "Ви можете скасувати лише власні замовлення.")


def test_cancel_order_conflict(
        client,
        login_admin,
        create_order,
        db
):
    order_id = create_order.id
    order = db.get(Order, order_id)

    assert order is not None

    create_order.status = OrderStatus.SHIPPED
    db.commit()
    db.refresh(create_order)

    db.expire_all()

    assert order.status.value == "shipped"

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=login_admin
    )

    assert response.status_code == 409
    assert (response.json()["detail"] ==
            "Замовлення не можна скасувати, "
            "оскільки його вже відправлено.")


def test_cancel_order_service_conflict(
        order_service,
        create_order,
        db
):
    create_order.status = OrderStatus.SHIPPED
    db.commit()
    db.refresh(create_order)

    user = db.scalar(
        select(User).where(User.username == "test_user")
    )
    order_id = create_order.id

    with pytest.raises(HTTPException) as exc_info:
        order_service.cancel_order(
            db,
            user,
            order_id
        )

    assert exc_info.value.status_code == 409
    assert (exc_info.value.detail
            == "Замовлення не можна скасувати, "
            "оскільки його вже відправлено.")


def test_cancel_order_bad_request(
        client,
        login_admin,
        create_order,
        db
):
    order_id = create_order.id
    order = db.get(Order, order_id)

    assert order is not None

    create_order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(create_order)

    db.expire_all()

    assert order.status.value == "cancelled"

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=login_admin
    )

    assert response.status_code == 400
    assert (response.json()["detail"] ==
            "Замовлення вже скасовано.")


def test_cancel_order_service_bad_request(
        order_service,
        create_order,
        db
):
    create_order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(create_order)

    user = db.scalar(
        select(User).where(User.username == "test_user")
    )
    order_id = create_order.id

    with pytest.raises(HTTPException) as exc_info:
        order_service.cancel_order(
            db,
            user,
            order_id
        )

    assert exc_info.value.status_code == 400
    assert (exc_info.value.detail
            == "Замовлення вже скасовано.")

def test_cancel_order_not_found(
        client,
        login_user,
        db
):
    response = client.patch(
        "/orders/999999/cancel",
        headers=login_user
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Замовлення не знайдено"


def test_cancel_order_service_not_found(
        order_service,
        db
):
    user = db.scalar(
        select(User).where(User.username == "test_user")
    )
    order_id = 99999

    with pytest.raises(HTTPException) as exc_info:
        order_service.cancel_order(
            db,
            user,
            order_id
        )

    assert exc_info.value.status_code == 404
    assert (exc_info.value.detail
            == "Замовлення не знайдено")
