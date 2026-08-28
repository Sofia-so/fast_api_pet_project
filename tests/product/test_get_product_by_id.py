from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import Product


def test_get_product_by_id_service(
        product_service,
        db
):
    product = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )

    assert product is not None

    result = product_service.get_product_by_id(db, product.id)

    assert result.id == product.id
    assert result.name == product.name
    assert result.description == product.description
    assert result.price == product.price
    assert result.status == product.status
    assert result.quantity == product.quantity
    assert result.category_id == product.category_id


def test_get_product_by_id_service_not_found(
        product_service,
        db
):
    with pytest.raises(HTTPException) as exc_info:
        product_service.get_product_by_id(db, 99999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Продукт не знайдено"
