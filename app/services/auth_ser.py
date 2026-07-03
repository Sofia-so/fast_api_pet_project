from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.authen.auth_passlib import (
    hash_password,
    verify_password
)
from app.db.model import User, BlacklistedToken
from app.schemas.user_schemas import UserCreateSchema
from app.schemas.message_schema import MessageResponseSchema

from app.authen.auth import create_token


class AuthService:

    def register(
            self,
            db: Session,
            user: UserCreateSchema,
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
            password=hash_password(user.password)
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Користувач з таким ім'ям або email вже існує."
            )

    def login(
            self,
            db: Session,
            form_data: OAuth2PasswordRequestForm
    ):

        db_user = db.query(User).filter(
            User.username == form_data.username
        ).first()

        if not db_user or not verify_password(
                form_data.password,
                db_user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Невірний логін або пароль"
            )

        token = create_token(db_user)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def logout(
            self,
            db: Session,
            token: str
    ):
        blacklisted_token = BlacklistedToken(token=token)

        db.add(blacklisted_token)
        db.commit()

        return MessageResponseSchema(
            message="Успішний вихід із системи."
        )


auth_service = AuthService()
