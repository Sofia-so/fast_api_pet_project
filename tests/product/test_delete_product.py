from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import Product, OrderItem


def test_delete_product(
        client,
        login_admin,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    response = client.delete(
        f"/products/{product_id}",
        headers=login_admin
    )

    db.expire_all()
    deleted_product = db.get(Product, product_id)

    assert response.status_code == 204
    assert deleted_product is None


def test_delete_product_service(
        product_service,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id
    product_service.delete_product(product_id, db)
    db.expire_all()

    deleted_product = db.get(Product, product_id)
    assert deleted_product is None


def test_delete_product_forbidden(
        client,
        login_admin,
        create_order,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    order_item = db.scalar(
        select(OrderItem)
        .where(OrderItem.product_id == product.id)
    )

    assert order_item is not None

    response = client.delete(
        f"/products/{product_id}",
        headers=login_admin
    )

    assert response.status_code == 409
    assert (response.json()["detail"]
            == "Неможливо видалити продукт, "
               "оскільки він використовується в замовленнях.")


def test_delete_product_service_forbidden(
        product_service,
        create_order,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    order_item = db.scalar(
        select(OrderItem)
        .where(OrderItem.product_id == product.id)
    )

    assert order_item is not None

    with pytest.raises(HTTPException) as exc_info:
        product_service.delete_product(
            product_id,
            db
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == (
        "Неможливо видалити продукт, "
        "оскільки він використовується в замовленнях."
    )


def test_delete_product_not_found(
        client,
        login_admin,
        db
):
    response = client.delete(
        "/products/99999",
        headers=login_admin
    )

    assert response.status_code == 404


def test_delete_product_without_access(
        client,
        login_user,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    response = client.delete(
        f"/products/{product_id}",
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"
