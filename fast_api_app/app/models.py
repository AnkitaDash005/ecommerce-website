from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base


class Product(Base):
    __tablename__ = "products_product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    stock = Column(Integer)
    image = Column(String)