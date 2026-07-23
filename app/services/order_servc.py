from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from decimal import Decimal
from sqlalchemy import select
import logging

from app.schemas.order_schemas import (
    OrderCreateSchema,
    OrderChangeStatusSchema
)
from app.db.model import (
    Order,
    User,
    Product,
    OrderItem
)
from app.order_number import generate_order_number
from app.db.model_enum import (
    ProductStatus,
    UserRole,
    OrderStatus
)
from app.constants import allowed_transitions

logger = logging.getLogger(__name__)


class OrderService:

    def create_order(
            self,
            db: Session,
            user: User,
            data: OrderCreateSchema
    ):
        order_data = data.model_dump(exclude={"items"})

        order = Order(
            **order_data,
            number=generate_order_number(),
            user_id=user.id
        )

        total_price = Decimal("0.00")

        db.add(order)

        for item in data.items:
            product = db.scalar(
                select(Product)
                .where(Product.id == item.product_id)
                .with_for_update()
            )

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Продукт з id={item.product_id} не знайдено"
                )

            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Недостатньо товару '{product.name}' на складі. "
                           f"Доступна кількість товару {product.quantity}"
                )

            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            order.items.append(order_item)
            total_price += item.quantity * product.price

            product.quantity -= item.quantity

            if product.quantity == 0:
                product.status = ProductStatus.OUT_OF_STOCK

        order.total_price = total_price

        try:
            db.commit()
            db.refresh(order)
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Unexpected error while creating order")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутрішня помилка сервера"
            )
        except Exception:
            db.rollback()
            raise

        return order

    def cancel_order(
            self,
            db: Session,
            user: User,
            order_id: int
    ):
        try:
            order = db.scalar(
                select(Order)
                .where(Order.id == order_id)
                .with_for_update()
            )

            if order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Замовлення не знайдено"
                )

            if user.role == UserRole.CLIENT:
                if order.user_id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Ви можете скасувати лише власні замовлення."
                    )

            if order.status == OrderStatus.SHIPPED:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Замовлення не можна скасувати, оскільки його вже відправлено."
                )

            if order.status == OrderStatus.CANCELLED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Замовлення вже скасовано."
                )

            order.status = OrderStatus.CANCELLED

            for item in order.items:
                product = db.scalar(
                   select(Product)
                    .where(Product.id == item.product_id)
                    .with_for_update()
                )

                if product is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Товар з id={item.product_id} не знайдено."
                    )

                product.quantity += item.quantity

                if product.quantity > 0:
                    product.status = ProductStatus.AVAILABLE

            db.commit()
            db.refresh(order)

        except HTTPException:
            db.rollback()
            raise

        except SQLAlchemyError:
            db.rollback()
            logger.exception("Unexpected error while cancelling the order")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутрішня помилка сервера"
            )
        except Exception:
            db.rollback()
            raise

        return order

    def get_orders(
            self,
            db: Session,
            user: User
    ):
        stmt = select(Order).order_by(Order.created_at.desc())

        if user.role == UserRole.CLIENT:
            stmt = stmt.where(Order.user_id == user.id)

        return db.scalars(stmt).all()

    def search_orders(
            self,
            db: Session,
            query: str
    ):
        orders = db.scalars(
            select(Order).where(
                Order.number.ilike(f"%{query}%")
            ).limit(10)
        ).all()

        return orders

    def get_order_by_number(
            self,
            db: Session,
            number: str
    ):
        order = db.scalar(
            select(Order).where(Order.number == number)
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Замовлення не знайдено."
            )

        return order

    def change_order_status(
            self,
            db: Session,
            number: str,
            data: OrderChangeStatusSchema
    ):
        order = self.get_order_by_number(db=db, number=number)
        new_status = data.status

        if new_status == order.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Замовлення вже має цей статус."
            )

        if new_status not in allowed_transitions.get(order.status, set()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Не можна змінити статус з "
                f"{order.status.value} на '{new_status.value}'."
            )

        try:
            order.status = new_status
            db.commit()
            db.refresh(order)
            return order
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while changing order status")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутрішня помилка сервера"
            )
        except Exception:
            db.rollback()
            logger.exception("Unexpected error while changing order status")
            raise


order_service = OrderService()