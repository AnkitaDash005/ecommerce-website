from app.schemas.product import Product
from pydantic import BaseModel


class ProductPagination(BaseModel):
    page: int
    limit: int
    total: int
    products: list[Product]

    class Config:
        from_attributes = True