from datetime import datetime

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    coupon: str | None = None

class OrderStatusUpdate(BaseModel):
    status: str