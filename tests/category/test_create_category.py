from sqlalchemy import select

from app.db.model import Category
from app.schemas.category_schemas import CategoryCreateSchema


def test_create_category_success(
        client,
        login_admin,
        db
):
    response = client.post(
        "/categories/",
        json={
            "name": "test_category_test",
            "description": "test_category"
        },
        headers=login_admin
    )

    response_json = response.json()

    assert response.status_code == 201

    category = db.scalar(
        select(Category).where(Category.name == "test_category_test")
    )

    assert category is not None
    assert response_json["name"] == category.name
    assert response_json["description"] == category.description


def test_create_category_service_success(
        category_service,
        db
):
    schema = CategoryCreateSchema(
        name="test_category_test",
        description="test category"
    )

    result = category_service.create_category(
        db,
        schema
    )

    category = db.scalar(
        select(Category).where(Category.name == "test_category_test")
    )

    assert category is not None
    assert result.name == category.name
    assert result.description == category.description


def test_create_category_duplicate_name(
        client,
        login_admin,
        db
):
    response = client.post(
        "/categories/",
        json={
            "name": "test_category1",
            "description": "test_category"
        },
        headers=login_admin
    )

    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None
    assert response.status_code == 400
    assert response.json()["detail"] == "Категорія з такою назвою вже існує"


def test_create_category_without_access(
        client,
        login_user
):
    response = client.post(
        "/categories/",
        json={
            "name": "test_category_test",
            "description": "test_category"
        },
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"
