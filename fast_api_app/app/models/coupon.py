from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String
)
from datetime import datetime

from app.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String,
        unique=True,
        nullable=False
    )

    discount = Column(
        Float,
        nullable=False
    )

    # percentage or flat
    discount_type = Column(
        String,
        nullable=False
    )

    expiry_date = Column(
        DateTime,
        nullable=False
    )

    minimum_amount = Column(
        Float,
        default=0
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )