from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    image = Column(String)

    # Foreign Key to Category
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )

    # Relationships
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    wishlist_items = relationship(
        "Wishlist",
        back_populates="product",
        cascade="all, delete-orphan"
    )