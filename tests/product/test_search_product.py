from sqlalchemy import select

from app.db.model import Product


def test_search_product(
        client,
        db
):
    response = client.get(
        "/products/search",
        params={"query": "test"}
    )

    products = db.scalars(
        select(Product).where(Product.name.ilike("%test%"))
        .order_by(Product.name).limit(10)
    ).all()
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == len(products)
    for response_product, product in zip(
        response_json, products
    ):
        assert response_product["id"] == product.id
        assert response_product["name"] == product.name
        assert response_product["description"] == product.description
        assert response_product["price"] == str(product.price)
        assert response_product["status"] == product.status.value
        assert response_product["quantity"] == product.quantity
        assert response_product["category_id"] == product.category_id


def test_search_product_service(
        product_service,
        db
):
    query = "test"
    result = product_service.search_product(query, db)
    products = db.scalars(
        select(Product).where(Product.name.ilike(f"%{query}%"))
        .order_by(Product.name).limit(10)
    ).all()

    assert len(result) == len(products)
    for result_product, product in zip(
            result,
            products):
        assert result_product.id == product.id
        assert result_product.name == product.name
        assert result_product.description == product.description
        assert result_product.price == product.price
        assert result_product.status == product.status
        assert result_product.quantity == product.quantity
        assert result_product.category_id == product.category_id
