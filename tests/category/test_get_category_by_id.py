from sqlalchemy import select
import pytest
from fastapi import HTTPException

from app.db.model import Category


def test_get_category_by_id_service_success(
        category_service,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    result = category_service.get_category_by_id(
        db,
        category.id
    )

    assert result.id == category.id
    assert result.name == category.name
    assert result.description == category.description


def test_get_category_by_id_service_not_found(
        category_service,
        db
):
    with pytest.raises(HTTPException) as exc_info:
        category_service.get_category_by_id(
            db,
            999999
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Категорію не знайдено"
