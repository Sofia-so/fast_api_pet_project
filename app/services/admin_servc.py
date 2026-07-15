from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.schemas.user_schemas import UserCreateSchema
from app.db.model import User
from app.db.model_enum import UserRole
from app.authen.auth_passlib import hash_password


class AdminService:
    def create_employee(
            self,
            db: Session,
            user: UserCreateSchema
    ):
        if len(user.password.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=400,
                detail="Пароль не може бути довшим за 72 байти."
            )

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            role=UserRole.EMPLOYEE
        )
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Користувач з таким ім'ям або email вже існує."
            )
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Помилка на сервері"
            )

    def delete_employee(
            self,
            db: Session,
            user: User
    ):
        if user.role != UserRole.EMPLOYEE:
            raise HTTPException(
                status_code=403,
                detail="Можна видаляти лише працівників."
            )
        try:
            db.delete(user)
            db.commit()

            return {
                "message": "Працівника успішно видалено"
            }
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Не вдалося видалити акаунт.")

    def get_list_employees(
            self,
            db: Session
    ):
        employees = db.scalars(select(User).where(
            User.role == UserRole.EMPLOYEE)
        ).all()
        return employees


admin_service = AdminService()