from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.schemas.user_schemas import (
    UserResponseSchema,
    UserCreateSchema
)
from app.schemas.message_schema import MessageResponseSchema
from app.authen.auth import get_current_admin
from app.db.session import get_db
from app.services.admin_servc import admin_service
from app.db.model import User

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.post(
    "/employee",
    response_model=UserResponseSchema,
    status_code=201,
    summary="Реєстрація робітника",
    description="""
    Створює нового працівника.
    Доступно лише користувачам із роллю "admin".
    Функціонал:
    - перевіряє унікальність username та email;
    - хешує пароль перед збереженням у базі даних;
    - призначає створеному користувачу роль "employee";
    - повертає інформацію про створеного користувача.
    """
)
def register_worker(
        user: UserCreateSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)

):
    return admin_service.create_employee(
        user=user,
        db=db
    )


@admin_router.delete(
    "/employee/{user_id}",
    response_model=MessageResponseSchema,
    status_code=200,
    summary="Видалення працівника",
    description="""
    Видаляє працівника за його ідентифікатором.

    Доступно лише користувачам із роллю "admin".
    """
)
def delete_employee(
        user_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Користувача не знайдено."
        )

    return admin_service.delete_employee(
        user = user,
        db=db
    )


@admin_router.get(
    "/employees",
    response_model=list[UserResponseSchema],
    status_code=200,
    summary="Отримати список усіх працівників",
    description="""
    Повертає список усіх працівників.
    Доступно лише користувачам із роллю "admin".
    """
)
def get_list_employees(
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    return admin_service.get_list_employees(
        db=db
    )
