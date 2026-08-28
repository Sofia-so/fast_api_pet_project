from sqlalchemy import select
from decimal import Decimal
import pytest
from fastapi import HTTPException

from app.db.model import Product
from app.schemas.product_schemas import ProductUpdateSchema


def test_update_product_success(
        client,
        login_admin,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    response = client.patch(
        f"/products/{product_id}",
        json={
            "description": "test",
            "price": "342.70"
        },
        headers=login_admin
    )

    db.expire_all()

    updated_product = db.get(Product, product_id)
    response_json = response.json()

    assert response.status_code == 200
    assert updated_product is not None
    assert response_json["id"] == updated_product.id
    assert response_json["name"] == updated_product.name
    assert response_json["description"] == updated_product.description
    assert response_json["price"] == str(updated_product.price)
    assert response_json["status"] == updated_product.status.value
    assert response_json["quantity"] == updated_product.quantity
    assert response_json["category_id"] == updated_product.category_id


def test_update_product_service_success(
        product_service,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id
    schema = ProductUpdateSchema(
        description="test",
        price=Decimal("342.70")
    )
    result = product_service.update_product(
        db,
        product_id,
        schema
    )

    db.expire_all()

    updated_product = db.get(Product, product_id)

    assert updated_product is not None
    assert result.id == updated_product.id
    assert result.name == updated_product.name
    assert result.description == updated_product.description
    assert result.price == updated_product.price
    assert result.status == updated_product.status
    assert result.quantity == updated_product.quantity
    assert result.category_id == updated_product.category_id


def test_update_product_duplicate_name(
        client,
        login_admin,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    response = client.patch(
        f"/products/{product_id}",
        json={
            "name": "test_product2",
            "description": "test",
            "price": "342.70"
        },
        headers=login_admin
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Продукт з такою назвою вже існує"


def test_update_product_service_duplicate_name(
        product_service,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id
    schema = ProductUpdateSchema(
        name="test_product2",
        description="test",
        price=Decimal("342.70")
    )
    with pytest.raises(HTTPException) as exc_info:
        product_service.update_product(
            db,
            product_id,
            schema
        )
    assert exc_info.value.status_code == 409
    assert (exc_info.value.detail
            == "Продукт з такою назвою вже існує")


def test_update_product_without_access(
        client,
        login_user,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    product_id = product.id

    response = client.patch(
        f"/products/{product_id}",
        json={
            "description": "test",
            "price": "342.70"
        },
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"


def test_update_product_bad_request(
        client,
        login_admin,
        db
):
    response = client.patch(
        "/products/99999",
        json={
            "description": "test",
            "price": "342.70"
        },
        headers=login_admin
    )

    assert response.status_code == 404
