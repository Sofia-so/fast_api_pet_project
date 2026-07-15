from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.schemas.message_schema import MessageResponseSchema
from app.schemas.user_schemas import (
    UserCreateSchema,
    UserResponseSchema
)
from app.schemas.token_schema import TokenSchema

from app.authen.oauth2_scheme import oauth2_scheme
from app.services.auth_servc import auth_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=201,
    summary="Реєстрація нового користувача",
    description="""
    Створює нового користувача.

    - перевіряє унікальність email та ім'я користувача;
    - хешує пароль перед збереженням;
    - повертає інформацію про створеного користувача.
    """
)
def register(
        user: UserCreateSchema,
        db: Session = Depends(get_db)
):
    return auth_service.register(
        db=db,
        user=user
    )


@auth_router.post(
    "/login",
    response_model=TokenSchema,
    status_code=200,
    summary="Авторизація користувача",
    description="""
    Перевіряє ім'я користувача та пароль.

    Якщо дані правильні, повертає JWT-токен,
    який використовується для доступу до захищених ендпоінтів.
    """
)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    return auth_service.login(
        db=db,
        form_data=form_data
    )


@auth_router.post(
    "/logout",
    response_model=MessageResponseSchema,
    status_code=200,
    summary="Вихід користувача",
    description="""
    Деактивує поточний JWT-токен.
    Після виходу цей токен більше не може використовуватися
    для доступу до захищених ендпоінтів.
    """
)
def logout(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    return auth_service.logout(
        db=db,
        token=token
    )
