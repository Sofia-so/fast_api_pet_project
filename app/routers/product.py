from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schemas import (
    ProductResponseSchema,
    ProductCreateSchema,
    ProductUpdateSchema
)
from app.db.session import get_db
from app.authen.auth import get_current_worker
from app.db.model import User
from app.services.product_servc import product_service

product_router = APIRouter(prefix="/product", tags=["Products"])


@product_router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=201,
    summary="Створити продукт",
    description="""
    Створює продукт.
    
    Функція до ступна лише користувачам з роллю "admin" або "employee".
    Видає помилку якщо продукт з такою назвою вже створено.
    Повертає створений продукт.
    """
)
def create_product(
        product_data: ProductCreateSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return product_service.create_product(
        product_data=product_data,
        db=db
    )


@product_router.get(
    "/",
    response_model=list[ProductResponseSchema],
    status_code=200,
    summary="Отримати всі продукти",
    description="Повертає список всіх продуктів"
)
def get_product(
        db: Session = Depends(get_db)
):
    return product_service.get_products(db=db)


@product_router.get(
    "/search",
    response_model=list[ProductResponseSchema],
    status_code=200,
    summary="Пошук продуктів",
    description="""
    Повертає список продуктів, назва яких містить переданий текст.

    Пошук виконується без врахування регістру.
    Максимальна кількість результатів — 10.
    """
)
def search_products(
        query: str,
        db: Session = Depends(get_db)
):
    return product_service.search_product(
        query=query,
        db=db
    )


@product_router.patch(
    "/{product_id}",
    response_model=ProductResponseSchema,
    status_code=200,
    summary="Оновити продукт",
    description="""
    Оновлює дані продукту.

    Доступно лише користувачам з роллю admin або employee.
    Повертає оновлений продукт.
    """
)
def update_product(
        product_id: int,
        product_data: ProductUpdateSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return product_service.update_product(
        product_id=product_id,
        product_data=product_data,
        db=db
    )


@product_router.delete(
    "/{product_id}",
    status_code=204,
    summary="Видалити продукт",
    description="""
    Видаляє продукт за його ідентифікатором.

    Доступно лише користувачам з ролями "admin" або "employee".
    Якщо продукт використовується в замовленнях, повертається помилка.
    """
)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_worker)
):
    return product_service.delete_product(
        product_id=product_id,
        db=db
    )
