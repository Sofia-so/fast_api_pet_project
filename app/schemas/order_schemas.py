import re
from pydantic import field_validator, Field
from decimal import Decimal
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.db.model_enum import DeliveryMethod, OrderStatus


class OrderItemSchema(BaseSchema):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreateSchema(BaseSchema):
    customer_first_name: str
    customer_last_name: str
    customer_phone: str
    delivery_method: DeliveryMethod
    items: list[OrderItemSchema] = Field(min_length=1)

    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, value) -> str:
        if not re.fullmatch(r"\+380\d{9}$", value):
            raise ValueError(
                "Номер має бути у форматі +380XXXXXXXXX"
            )
        return value


class OrderItemResponseSchema(OrderItemSchema):
    product_name: str
    price: Decimal = Field(gt=0, decimal_places=2)


class OrderResponseSchema(BaseSchema):
    id: int
    number: str
    status: OrderStatus
    total_price: Decimal = Field(gt=0, decimal_places=2)
    created_at: datetime
    user_id: int
    customer_first_name: str
    customer_last_name: str
    customer_phone: str
    delivery_method: DeliveryMethod
    items: list[OrderItemResponseSchema]


class OrderChangeStatusSchema(BaseSchema):
    status: OrderStatus
