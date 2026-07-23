from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.schemas.category_schemas import (
    CategoryResponseSchema,
    CategoryCreateSchema,
    CategoryUpdateSchema
)
from app.db.session import get_db
from app.db.model import User
from app.authen.auth import get_current_admin
from app.services.category_servc import category_service

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=201,
    summary="Створити категорію",
    description="""
    Створює категорію.

    Функція доступна лише користувачам з роллю "admin".
    Видає помилку, якщо категорія з такою назвою вже існує.
    Повертає створену категорію.
    """
)
def create_category(
        category_data: CategoryCreateSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    return category_service.create_category(
        db=db,
        category_data=category_data
    )


@category_router.get(
    "/",
    response_model=list[CategoryResponseSchema],
    status_code=200,
    summary="Отримати всі категорій",
    description="Повертає всі категорії"
)
def get_categories(
        db: Session = Depends(get_db)
):
    return category_service.get_categories(db=db)


@category_router.get(
    "/search",
    response_model=list[CategoryResponseSchema],
    status_code=200,
    summary="Пошук категорій",
    description="""
    Повертає список категорій, назва яких відповідає пошуковому запиту.
    
    Пошук виконується без врахування регістру.
    Максимальна кількість результатів — 10.
    """
)
def categories_search(
        query: str,
        db: Session = Depends(get_db)
):
    return category_service.search_categories(
        query=query,
        db=db
    )


@category_router.patch(
    "/{category_id}",
    response_model=CategoryResponseSchema,
    status_code=200,
    summary="Оновлення категорії",
    description="""
    Оновлює категорію за ідентифікатором.

    Функція доступна лише користувачам з роллю "admin".
    Видає помилку, якщо категорія з такою назвою вже існує.
    Повертає оновлену категорію.
    """
)
def category_update(
        category_id: int,
        category_data: CategoryUpdateSchema,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    return category_service.category_update(
        category_id=category_id,
        category_data=category_data,
        db=db
    )


@category_router.delete(
    "/{category_id}",
    status_code=204,
    summary="Видалити категорію",
    description="""
    Видаляє категорію за ідентифікатором.

    Функція доступна лише користувачам з роллю "admin".
    Повертає помилку, якщо категорію не знайдено або вона містить товари.
    """
)
def category_delete(
        category_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    return category_service.category_delete(
        category_id=category_id,
        db=db
    )
