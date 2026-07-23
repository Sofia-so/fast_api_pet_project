from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
   ForeignKey,
   Enum,
   Numeric,
   String
)
from decimal import Decimal
from datetime import datetime

from app.db.model_enum import (
    ProductStatus,
    UserRole,
    OrderStatus,
    DeliveryMethod
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda enum: [
            item.value for item in enum
        ]),
        nullable=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

    def __repr__(self):
        return (f"User: username{self.username}")


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return (f"BlacklistedToken: token= {self.token[:10]}...")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(nullable=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"Category name - {self.name}"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    status: Mapped[ProductStatus] = mapped_column(
        Enum(
            ProductStatus,
            values_callable=lambda enum: [
            item.value for item in enum
        ]),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"Product name - {self.name}"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            OrderStatus,
            values_callable=lambda enum: [
                item.value for item in enum
            ]),
        default=OrderStatus.PENDING,
        nullable=False
    )
    customer_first_name: Mapped[str] = mapped_column(nullable=False)
    customer_last_name: Mapped[str] = mapped_column(nullable=False)
    customer_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=False
    )
    delivery_method: Mapped[DeliveryMethod] = mapped_column(
        Enum(
            DeliveryMethod,
             values_callable=lambda enum: [
                 item.value for item in enum
             ]),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped[User] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")

    def __repr__(self):
        return f"<Order {self.number}>"


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    product: Mapped["Product"] = relationship(back_populates="order_items")
    order: Mapped[Order] = relationship(back_populates="items")

    @property
    def product_name(self) -> str:
        return self.product.name

    def __repr__(self):
        return f"<OrderItem {self.id}>"
