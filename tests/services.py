import pytest

from app.services.auth_servc import AuthService
from app.services.user_servc import UserService
from app.services.admin_servc import AdminService


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def admin_service():
    return AdminService()