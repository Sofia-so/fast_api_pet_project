from sqlalchemy import select

from app.db.model import Category


def test_search_categories(
        client,
        db
):
    response = client.get(
        "/categories/search",
        params={"query": "test"}
    )

    categories = db.scalars(
        select(Category).where(Category.name.ilike("%test%"))
        .order_by(Category.name)
        .limit(10)
    ).all()

    assert response.status_code == 200
    assert len(categories) == len(response.json())

    for response_category, category in zip(
            response.json(),
            categories
    ):
        assert response_category["id"] == category.id
        assert response_category["name"] == category.name
        assert response_category["description"] == category.description


def test_search_categories_service(
        category_service,
        db
):
    query = "test"
    result = category_service.search_categories(
        db,
        query
    )

    categories = db.scalars(
        select(Category).where(Category.name.ilike("%test%"))
        .order_by(Category.name)
        .limit(10)
    ).all()


    assert len(categories) == len(result)

    for result_category, category in zip(
            result,
            categories
    ):
        assert result_category.id == category.id
        assert result_category.name == category.name
        assert result_category.description == category.description
