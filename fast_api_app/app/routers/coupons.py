from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.coupon import Coupon
from app.schemas.coupon import (
    CouponCreate,
    CouponResponse,
)

router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Coupon
@router.post(
    "/",
    response_model=CouponResponse,
    status_code=status.HTTP_201_CREATED
)
def create_coupon(
    coupon: CouponCreate,
    db: Session = Depends(get_db)
):
    existing_coupon = (
        db.query(Coupon)
        .filter(Coupon.code == coupon.code)
        .first()
    )

    if existing_coupon:
        raise HTTPException(
            status_code=400,
            detail="Coupon code already exists"
        )

    new_coupon = Coupon(
        code=coupon.code,
        discount=coupon.discount,
        discount_type=coupon.discount_type,
        expiry_date=coupon.expiry_date,
        minimum_amount=coupon.minimum_amount,
        is_active=coupon.is_active
    )

    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return new_coupon


# Get All Coupons
@router.get(
    "/",
    response_model=list[CouponResponse]
)
def get_coupons(
    db: Session = Depends(get_db)
):
    return db.query(Coupon).all()


# Delete Coupon
@router.delete("/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db)
):
    coupon = (
        db.query(Coupon)
        .filter(Coupon.id == coupon_id)
        .first()
    )

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found"
        )

    db.delete(coupon)
    db.commit()

    return {
        "message": "Coupon deleted successfully"
    }