import pytest

from app.services.auth_servc import AuthService


@pytest.fixture
def auth_service():
    return AuthService()
