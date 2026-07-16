from decimal import Decimal
from pydantic import Field

from app.schemas.base_schema import BaseSchema
from app.db.model_enum import ProductStatus

class ProductCreateSchema(BaseSchema):
    name: str
    description: str | None = None
    price: Decimal = Field(gt=0, decimal_places=2)
    status: ProductStatus
    quantity: int
    category_id: int


class ProductResponseSchema(ProductCreateSchema):
    id: int


class ProductUpdateSchema(BaseSchema):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2
    )
    status: ProductStatus | None = None
    quantity: int | None = None
    category_id: int | None = None
