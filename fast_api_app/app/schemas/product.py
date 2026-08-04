from app.schemas.category import CategoryResponse
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image: str | None = None


class ProductCreate(ProductBase):
    category_id: int | None = None


class Product(ProductBase):
    id: int
    average_rating: float | None = None
    category: CategoryResponse | None = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image: str | None = None
    average_rating: float | None = None

    class Config:
        from_attributes = True


class StockUpdate(BaseModel):
    stock: int = Field(..., ge=0)