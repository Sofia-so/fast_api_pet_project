import pytest
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

from app.main import app
from tests.override_get_db import override_get_db
from app.db.session import get_db
from app.config import settings


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def init_db():
    alembic_cfg = Config("alembic.ini")

    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.test_database_uri,
    )

    command.upgrade(alembic_cfg, "head")

    yield

    command.downgrade(alembic_cfg, "base")
