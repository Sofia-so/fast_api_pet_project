from sqlalchemy import select
from decimal import Decimal
import pytest
from fastapi import HTTPException

from app.db.model import Category, Product
from app.schemas.product_schemas import ProductCreateSchema
from app.db.model_enum import ProductStatus


def test_create_product_success(
        client,
        login_employee,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    response = client.post(
        "/products/",
        json={
            "name": "test_product_test",
            "description": "test_product",
            "price": "2354.78",
            "status": "available",
            "quantity": 13,
            "category_id": category.id
        },
        headers=login_employee
    )
    product = db.scalar(
        select(Product).where(Product.name == "test_product_test")
    )
    response_json = response.json()

    assert response.status_code == 201
    assert product is not None
    assert response_json["name"] == product.name
    assert response_json["description"] == product.description
    assert response_json["price"] == str(product.price)
    assert response_json["status"] == product.status.value
    assert response_json["quantity"] == product.quantity
    assert response_json["category_id"] == product.category_id


def test_create_product_service_success(
        product_service,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    product_data = ProductCreateSchema(
        name = "test_product_test",
        description = "test_product",
        price = Decimal("2354.78"),
        status = ProductStatus.AVAILABLE,
        quantity = 13,
        category_id = category.id
    )

    result = product_service.create_product(db, product_data)

    product = db.scalar(
        select(Product).where(Product.name == "test_product_test")
    )

    assert product is not None
    assert result.id == product.id
    assert result.name == product.name
    assert result.description == product.description
    assert result.price == product.price
    assert result.status == product.status
    assert result.quantity == product.quantity
    assert result.category_id == product.category_id


def test_create_product_duplicate_name(
        client,
        login_employee,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    response = client.post(
        "/products/",
        json={
            "name": "test_product1",
            "description": "test_product",
            "price": "2354.78",
            "status": "available",
            "quantity": 13,
            "category_id": category.id
        },
        headers=login_employee
    )

    response_json = response.json()

    assert response.status_code == 409
    assert response_json["detail"] == "Продукт з такою назвою вже існує"


def test_create_product_duplicate_name_service(
        product_service,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    product_data = ProductCreateSchema(
        name="test_product1",
        description="test_product",
        price=Decimal("2354.78"),
        status=ProductStatus.AVAILABLE,
        quantity=13,
        category_id=category.id
    )

    with pytest.raises(HTTPException) as exc_info:
        product_service.create_product(
            db,
            product_data
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Продукт з такою назвою вже існує"


def test_create_product_without_access(
        client,
        login_user,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    response = client.post(
        "/products/",
        json={
            "name": "test_product_test",
            "description": "test_product",
            "price": "2354.78",
            "status": "available",
            "quantity": 13,
            "category_id": category.id
        },
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"


def test_create_product_without_auth(
        client,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    response = client.post(
        "/products/",
        json={
            "name": "test_product_test",
            "description": "test_product",
            "price": "2354.78",
            "status": "available",
            "quantity": 13,
            "category_id": category.id
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
