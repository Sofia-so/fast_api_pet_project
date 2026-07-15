import os
from dotenv import load_dotenv
from sqlalchemy import select

from app.db.engine import SessionLocal
from app.db.model import User
from app.authen.auth_passlib import hash_password
from app.db.model_enum import UserRole


def create_admin():
    load_dotenv()
    db = SessionLocal()
    admin_password = os.getenv("ADMIN_PASSWORD")
    user = db.scalar(
    select(User).where(User.username == "admin")
    )
    if user is not None:
        return "Адміністратора вже створено."
    admin = User(
        first_name="admin",
        last_name="admin",
        username="admin",
        email="storeadmin@g.com",
        password=hash_password(admin_password),
        role=UserRole.ADMIN
    )
    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except Exception as e:
        db.rollback()
        return f"Виникла помилка: {e}"
    finally:
        db.close()


if __name__ == "__main__":
    print(create_admin())
