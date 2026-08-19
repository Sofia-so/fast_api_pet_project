import pytest
from sqlalchemy import delete, select
from decimal import Decimal

from app.db.model import (
    User,
    Category,
    Product,
    Order,
    OrderItem
)
from app.db.model_enum import (
    UserRole,
    ProductStatus,
    OrderStatus,
    DeliveryMethod
)
from app.authen.auth_passlib import hash_password


@pytest.fixture(scope="function", autouse=True)
def create_users(db):

    password = "strong password"

    test_user = User(
        first_name="test_user",
        last_name="test_user",
        username="test_user",
        email="email_user@test.com",
        password=hash_password(password),
        role=UserRole.CLIENT
    )

    test_employee = User(
        first_name="test_employee",
        last_name="test_employee",
        username="test_employee",
        email="email_employee@test.com",
        password=hash_password(password),
        role=UserRole.EMPLOYEE
    )

    test_admin = User(
        first_name="test_admin",
        last_name="test_admin",
        username="test_admin",
        email="email_admin@test.com",
        password=hash_password(password),
        role=UserRole.ADMIN
    )

    db.add_all([
        test_user,
        test_employee,
        test_admin
    ])
    db.commit()

    yield

    db.execute(delete(User))
    db.commit()


@pytest.fixture(scope="function", autouse=True)
def create_categories(db):

    category1 = Category(
        name="test_category1",
        description="test_category"
    )

    category2 = Category(
        name="test_category2",
        description="test_category"
    )

    db.add_all([category1, category2])
    db.commit()

    yield

    db.execute(delete(Category))
    db.commit()


@pytest.fixture(scope="function", autouse=True)
def create_products(db):

    category1 = db.scalar(
        select(Category).where(Category.name == "test_category1")
    )

    category2 = db.scalar(
        select(Category).where(Category.name == "test_category2")
    )

    product1 = Product(
        name="test_product1",
        description="test_product",
        price=Decimal("2354.78"),
        status=ProductStatus.AVAILABLE,
        quantity=13,
        category_id=category1.id
    )

    product2 = Product(
        name="test_product2",
        description="test_product",
        price=Decimal("154.00"),
        status=ProductStatus.AVAILABLE,
        quantity=4,
        category_id=category2.id
    )

    db.add_all([product1, product2])
    db.commit()

    yield

    db.execute(delete(Product))
    db.commit()


@pytest.fixture
def create_order(db):

    user = db.scalar(
        select(User).where(User.username == "test_user")
    )

    product1 = db.scalar(
        select(Product).where(Product.name == "test_product1")
    )
    product2 = db.scalar(
        select(Product).where(Product.name == "test_product2")
    )

    order = Order(
        number="ORD-001",
        status=OrderStatus.PENDING,
        customer_first_name="test client",
        customer_last_name="test client",
        customer_phone="+3800000000",
        delivery_method=DeliveryMethod.PICKUP,
        total_price=2 * product1.price + 2 * product2.price,
        user_id=user.id
    )
    order.items.extend([
        OrderItem(
            product=product1,
            quantity=2,
            price=product1.price
        ),
        OrderItem(
            product=product2,
            quantity=2,
            price=product2.price
        )
    ])

    db.add(order)
    db.commit()

    yield

    db.execute(delete(OrderItem))
    db.execute(delete(Order))
    db.commit()
