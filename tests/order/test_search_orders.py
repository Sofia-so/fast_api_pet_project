from sqlalchemy import select
from decimal import Decimal

from app.db.model import Order


def test_search_orders(
        client,
        login_employee,
        create_order,
        db
):
    response = client.get(
        "/orders/search",
        params={"query": "ORD"},
        headers=login_employee
    )

    orders = db.scalars(
            select(Order).where(
                Order.number.ilike(f"%ORD%")
            )
            .order_by(Order.created_at.desc()).limit(10)
        ).all()

    response_json = response.json()

    assert response.status_code == 200

    assert len(response_json) == len(orders)

    for order, response_order in zip(orders, response_json):
        assert (response_order["customer_first_name"]
                == order.customer_first_name)
        assert (response_order["customer_last_name"]
                == order.customer_last_name)
        assert (response_order["customer_phone"]
                == order.customer_phone)
        assert (response_order["delivery_method"]
                == order.delivery_method.value)
        assert response_order["number"] == order.number
        assert response_order["status"] == order.status.value
        assert (Decimal(response_order["total_price"])
                == order.total_price)
        assert (response_order["created_at"]
                == order.created_at.isoformat())
        assert response_order["user_id"] == order.user_id


def test_search_orders_service(
        order_service,
        create_order,
        db
):
    query = "ORD"

    orders = db.scalars(
        select(Order).where(
            Order.number.ilike(f"%ORD%")
        )
        .order_by(Order.created_at.desc()).limit(10)
    ).all()

    result = order_service.search_orders(db, query)

    assert len(orders) == len(result)

    for order, result_order in zip(orders, result):
        assert (result_order.customer_first_name
                == order.customer_first_name)
        assert (result_order.customer_last_name
                == order.customer_last_name)
        assert (result_order.customer_phone
                == order.customer_phone)
        assert (result_order.delivery_method
                == order.delivery_method)
        assert result_order.number == order.number
        assert result_order.status == order.status
        assert result_order.total_price == order.total_price
        assert (result_order.created_at
                == order.created_at)
        assert result_order.user_id == order.user_id


def test_search_orders_forbidden(
        client,
        login_user,
        db
):
    response = client.get(
        "/orders/search",
        params={"query": "ORD"},
        headers=login_user
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостатньо прав доступу"
