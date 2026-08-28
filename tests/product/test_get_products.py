from sqlalchemy import select

from app.db.model import Product


def test_get_products(
        client,
        db
):
    response = client.get(
        "/products/"
    )

    products = db.scalars(
        select(Product).order_by(Product.name)
    ).all()

    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == len(products)
    for response_product, product in zip(
            response_json,
            products):
        assert response_product["id"] == product.id
        assert response_product["name"] == product.name
        assert response_product["description"] == product.description
        assert response_product["price"] == str(product.price)
        assert response_product["status"] == product.status.value
        assert response_product["quantity"] == product.quantity
        assert response_product["category_id"] == product.category_id


def test_get_products_service(
        product_service,
        db
):
    result = product_service.get_products(db)

    products = db.scalars(
        select(Product).order_by(Product.name)
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
