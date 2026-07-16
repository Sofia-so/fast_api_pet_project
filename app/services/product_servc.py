from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select

from app.schemas.product_schemas import (
    ProductCreateSchema,
    ProductUpdateSchema
)
from app.db.model import Product, Category


class ProductService:

    def create_product(
            self,
            db: Session,
            product_data: ProductCreateSchema
    ):
        category = db.get(Category, product_data.category_id)
        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Категорію не знайдено"
            )
        try:
            product = Product(
                **product_data.model_dump()
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Продукт з такою назвою вже існує"
            )

    def get_products(
            self,
            db: Session,
    ):
        products = db.scalars(
            select(Product)
        ).all()
        return products

    def search_product(
            self,
            query: str,
            db: Session
    ):
        products = db.scalars(
            select(Product).where(Product.name.ilike(
                f"%{query}%")
            ).limit(10)
        ).all()
        return products

    def get_product_by_id(
            self,
            db: Session,
            product_id: int
    ):
        product = db.get(Product, product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Продукт не знайдено"
            )
        return product

    def update_product(
            self,
            db: Session,
            product_id: int,
            product_data: ProductUpdateSchema
    ):
        product = self.get_product_by_id(
            db=db,
            product_id=product_id
        )
        try:
            for key, value in product_data.model_dump(
                    exclude_unset=True
            ).items():
                setattr(product, key, value)
            db.commit()
            db.refresh(product)
            return product
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Продукт з такою назвою вже існує"
            )

    def delete_product(
            self,
            product_id: int,
            db: Session
    ):
        product = self.get_product_by_id(
            db=db,
            product_id=product_id
        )
        try:
            db.delete(product)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="""
                Неможливо видалити продукт,
                скільки він використовується в замовленнях.
                """
            )


product_service = ProductService()
