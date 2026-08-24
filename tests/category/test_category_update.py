from sqlalchemy import select

from app.db.model import Category
from app.schemas.category_schemas import CategoryUpdateSchema


def test_category_update_success(
        client,
        login_admin,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    response = client.patch(
        f"/categories/{category.id}",
        json={
            "name": "updated_category"
        },
        headers=login_admin
    )
    response_json = response.json()

    db.expire_all()

    updated_category = db.get(Category, category.id)

    assert response.status_code == 200
    assert updated_category is not None
    assert response_json["id"] == updated_category.id
    assert response_json["name"] == updated_category.name
    assert response_json["description"] == updated_category.description


def test_category_update_service_success(
        category_service,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    schema = CategoryUpdateSchema(
        name="updated_category"
    )

    result = category_service.category_update(
        db,
        category.id,
        schema
    )

    assert result.id == category.id
    assert result.name == "updated_category"
    assert result.description == category.description


def test_category_update_duplicate_name(
        client,
        login_admin,
        db
):
    category1 = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    category2 = db.scalar(
        select(Category).where(Category.name == "test_category2")
    )

    assert category1 is not None
    assert category2 is not None

    response = client.patch(
        f"/categories/{category1.id}",
        json={
            "name": "test_category2"
        },
        headers=login_admin
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Категорія з такою назвою вже існує"


def test_category_update_without_access(
        client,
        login_employee,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    response = client.patch(
        f"/categories/{category.id}",
        json={
            "name": "updated_category"
        },
        headers=login_employee
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"
