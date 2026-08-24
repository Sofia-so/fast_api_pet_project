from sqlalchemy import select, delete

from app.db.model import Category, Product


def test_category_delete_success(
        client,
        login_admin,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    category_id = category.id

    db.execute(
        delete(Product).where(
            Product.category_id == category_id
        )
    )
    db.commit()

    response = client.delete(
        f"/categories/{category_id}",
        headers=login_admin
    )

    assert response.status_code == 204


def test_category_delete_service_success(
        category_service,
        db
):
    category = db.scalar(
        select(Category).where(
            Category.name == "test_category1"
        )
    )

    assert category is not None

    category_id = category.id

    db.execute(
        delete(Product).where(
            Product.category_id == category_id
        )
    )

    result = category_service.category_delete(
        db,
        category_id
    )

    deleted_category = db.get(
        Category,
        category_id
    )

    assert result is None
    assert deleted_category is None


def test_category_delete_with_product(
        client,
        login_admin,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    category_id = category.id

    response = client.delete(
        f"/categories/{category_id}",
        headers=login_admin
    )

    assert response.status_code == 400
    assert (response.json()["detail"]
            == "Неможливо видалити категорію, "
               "оскільки вона містить товари.")


def test_category_delete_without_access(
        client,
        login_user,
        db
):
    category = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    assert category is not None

    db.execute(
        delete(Product).where(
            Product.category_id == category.id
        )
    )
    db.commit()

    category_id = category.id

    response = client.delete(
        f"/categories/{category_id}",
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"
