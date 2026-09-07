import pytest

from app.services.auth_servc import AuthService
from app.services.user_servc import UserService
from app.services.admin_servc import AdminService
from app.services.category_servc import CategoryService
from app.services.product_servc import ProductService
from app.services.order_servc import OrderService


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def admin_service():
    return AdminService()


@pytest.fixture
def category_service():
    return CategoryService()


@pytest.fixture
def product_service():
    return ProductService()


@pytest.fixture
def order_service():
    return OrderService()
