from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    image: str

    model_config = ConfigDict(from_attributes=True)