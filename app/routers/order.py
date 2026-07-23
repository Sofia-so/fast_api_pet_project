from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.orm import Session

from app.schemas.order_schemas import (
    OrderResponseSchema,
    OrderCreateSchema,
    OrderChangeStatusSchema
)
from app.authen.auth import (
    get_current_user,
    get_current_worker
)
from app.db.model import User
from app.db.session import get_db
from app.services.order_servc import order_service

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post(
    "/",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Оформлення замовлення",
    description="""
    Оформлює замовлення.

    Доступно лише для авторизованих користувачів.

    Перевіряє наявність товарів і їх доступну кількість на складі, 
    розраховує загальну вартість замовлення, 
    оновлює залишки та статус товарів при необхідності.
    Повертає інформацію про створене замовлення.
    """
)
def create_order(
        data: OrderCreateSchema,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return order_service.create_order(
        data=data,
        user=user,
        db=db
    )


@order_router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Скасування замовлення",
    description="""
    Скасовує замовлення.

    Доступно авторизованим користувачам.
    Користувач із роллю "client" може скасувати лише власне замовлення.
    Користувачі з ролями "admin" та "employee" можуть скасувати будь-яке замовлення.

    Повертає товари на склад, змінює статус замовлення на "CANCELLED" 
    та повертає оновлену інформацію про замовлення.
    """
)
def cancel_order(
        order_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return order_service.cancel_order(
        order_id=order_id,
        user=user,
        db=db
    )


@order_router.get(
    "/",
    response_model=list[OrderResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Отримати список замовлень",
    description="""
    Повертає список замовлень.
    
    Користувачі з ролями "admin" та "employee"
    отримують усі замовлення.
    
    Користувач із роллю "client"
    отримує лише власні замовлення.
    """
)
def get_orders(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return order_service.get_orders(
        user=user,
        db=db
    )


@order_router.get(
    "/search",
    response_model=list[OrderResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Пошук замовлення",
    description="""
    Повертає список замовлень, номер яких містить введений пошуковий рядок.

    Доступно лише користувачам з ролями "admin" та "employee".
    """
)
def search_orders(
        query: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return order_service.search_orders(
        query=query,
        db=db
    )


@order_router.get(
    "/{number}",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Отримати замовлення за номером",
    description="""
    Повертає інформацію про замовлення за його номером.

    Доступно лише користувачам з ролями "admin" та "employee".
    """
)
def get_order_by_number(
        number: str,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return order_service.get_order_by_number(
        number=number,
        db=db
    )


@order_router.patch(
    "/{number}/status",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Змінити статус замовлення",
    description="""
    Змінює статус замовлення.

    Доступно лише користувачам з ролями "admin" та "employee"
    """
)
def change_order_status(
        number: str,
        data: OrderChangeStatusSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return order_service.change_order_status(
        number=number,
        data=data,
        db=db
    )
