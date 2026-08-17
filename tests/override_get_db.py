from app.db.engine import TestSessionLocal


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
        