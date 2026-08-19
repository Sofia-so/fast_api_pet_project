import pytest

from app.services.auth_servc import AuthService
from app.services.user_servc import UserService


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def user_service():
    return UserService()
