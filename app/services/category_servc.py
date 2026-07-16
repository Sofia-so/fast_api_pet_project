from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select

from app.schemas.category_schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema
)
from app.db.model import Category


class CategoryService:

    def create_category(
            self,
            db: Session,
            category_data: CategoryCreateSchema
    ):
        try:
            category = Category(
                **category_data.model_dump()
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Категорія з такою назвою вже існує"
            )

    def get_categories(
            self,
            db: Session
    ):
        categories = db.scalars(
            select(Category)
        ).all()
        return categories

    def search_categories(
            self,
            db: Session,
            query: str
    ):
        return db.scalars(
            select(Category)
            .where(Category.name.ilike(f"%{query}%"))
            .limit(10)
        ).all()

    def get_category_by_id(
            self,
            db: Session,
            category_id: int
    ):
        category = db.get(Category, category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Категорію не знайдено"
            )

        return category

    def category_update(
            self,
            db: Session,
            category_id: int,
            category_data: CategoryUpdateSchema
    ):
        category = self.get_category_by_id(
            db=db,
            category_id=category_id
        )
        update_data = category_data.model_dump(exclude_unset=True)
        try:
            for key, value in update_data.items():
                setattr(category, key, value)
            db.commit()
            db.refresh(category)
            return category
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Категорія з такою назвою вже існує"
            )

    def category_delete(
            self,
            db: Session,
            category_id: int
    ):
        category = self.get_category_by_id(
            db=db,
            category_id=category_id
        )
        try:
            db.delete(category)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Неможливо видалити категорію, оскільки вона містить товари."
            )


category_service = CategoryService()
