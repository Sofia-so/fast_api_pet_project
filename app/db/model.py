from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
   ForeignKey,
   Enum,
   Numeric
)
from decimal import Decimal

from app.db.model_enum import ProductStatus, UserRole


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

    def __repr__(self):
        return f"Product name - {self.name}"
