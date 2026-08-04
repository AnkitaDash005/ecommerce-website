from datetime import datetime

from pydantic import BaseModel, Field


class CouponBase(BaseModel):
    code: str
    discount: float = Field(..., gt=0)
    discount_type: str
    expiry_date: datetime
    minimum_amount: float = Field(default=0, ge=0)
    is_active: bool = True


class CouponCreate(CouponBase):
    pass


class CouponResponse(CouponBase):
    id: int

    class Config:
        from_attributes = True