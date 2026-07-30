from sqlalchemy import Column, Integer, String, Float

from app.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products_product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    image = Column(String)
    cart_items = relationship("CartItem", back_populates="product")