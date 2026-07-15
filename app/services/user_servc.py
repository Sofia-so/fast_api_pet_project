from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.user_schemas import (
    UserChangePasswordSchema,
    UserBaseSchema
)
from app.authen.auth_passlib import (
    verify_password,
    hash_password
)
from app.db.model import User


class UserService:

    def change_password(
            self,
            db: Session,
            current_user: User,
            password_data: UserChangePasswordSchema
    ):
        if len(password_data.new_password.encode("utf8")) > 72:
            raise HTTPException(
                status_code=400,
                detail="Пароль не може бути довшим за 72 байти."
            )

        if not verify_password(
                password_data.current_password,
                current_user.password,
        ):
            raise HTTPException(
                status_code=400,
                detail="Невірний пароль"
            )

        current_user.password = hash_password(password_data.new_password)

        db.commit()
        db.refresh(current_user)

        return {"message": "Пароль успішно змінено."}

    def update_user(
            self,
            db: Session,
            current_user: User,
            user_data: UserBaseSchema
    ):
        update_data = user_data.model_dump(exclude_unset=True)
        try:
            for key, values in update_data.items():
                setattr(current_user, key, values)

            db.commit()
            db.refresh(current_user)

            return {
                "message": "Дані користувача успішно оновлено."
            }

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Користувач з таким ім'ям або email вже існує."
            )

    def profile(
            self,
            current_user: User,
    ):
        return current_user

    def delete_user(
            self,
            db: Session,
            current_user: User
    ):
        try:
            db.delete(current_user)
            db.commit()

            return {
                "message": "Акаунт успішно видалено"
            }
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Не вдалося видалити акаунт.")


user_service = UserService()
