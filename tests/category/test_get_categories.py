from sqlalchemy import select

from app.db.model import Category


def test_get_categories(
        client,
        db
):
    response = client.get(
        "/categories/"
    )

    categories = db.scalars(
        select(Category).order_by(Category.name)
    ).all()
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == len(categories)

    for response_category, category in zip(response_json, categories):
        assert response_category["id"] == category.id
        assert response_category["name"] == category.name
        assert response_category["description"] == category.description


def test_get_categories_service(
        category_service,
        db
):
    result = category_service.get_categories(db)

    categories = db.scalars(
        select(Category)
        .order_by(Category.id)
    ).all()

    assert len(result) == len(categories)

    for result_category, category in zip(result, categories):
        assert result_category.id == category.id
        assert result_category.name == category.name
        assert result_category.description == category.description
