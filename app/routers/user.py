from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schemas import (
    UserResponseSchema,
    UserChangePasswordSchema,
    UserUpdateSchema
)
from app.schemas.message_schema import MessageResponseSchema
from app.db.session import get_db
from app.authen.auth import get_current_user
from app.db.model import User
from app.services.user_servc import user_service

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.patch(
    "/password",
    response_model=MessageResponseSchema,
    status_code=200,
    summary="Змінити пароль користувача",
    description="""
    Змінює пароль авторизованого користувача.
    Необхідно вказати поточний пароль та новий пароль.
    """
)
def change_password(
        password_data: UserChangePasswordSchema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return user_service.change_password(
        db=db,
        current_user=current_user,
        password_data=password_data
    )


@user_router.patch(
    "/me",
    response_model=MessageResponseSchema,
    status_code=200,
    summary="Оновити дані користувача",
    description="""
    Оновлює дані авторизованого користувача.

    Перевіряє унікальність імені користувача та email.
    Повертає повідомлення про успішне оновлення.
    """
)
def update_user(
        user_data: UserUpdateSchema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return user_service.update_user(
        user_data=user_data,
        db=db,
        current_user=current_user
    )


@user_router.get(
    "/me",
    response_model=UserResponseSchema,
    status_code=200,
    summary="Отримати профіль користувача",
    description="Повертає дані авторизованого користувача."
)
def profile(current_user: User = Depends(get_current_user)):
    return user_service.profile(current_user=current_user)


@user_router.delete(
    "/me",
    response_model=MessageResponseSchema,
    status_code=200,
    summary="Видалити профіль користувача",
    description="""
    Видаляє обліковий запис авторизованого користувача.
    Після успішного видалення повертає повідомлення про успішне виконання операції.
    """
)
def delete_user(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return user_service.delete_user(db=db, current_user=current_user)
