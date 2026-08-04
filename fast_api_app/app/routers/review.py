from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import SessionLocal
from app.models.product import Product
from app.models.reviews import Review

from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
)

router = APIRouter(
    tags=["Reviews"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Review
@router.post(
    "/products/{product_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED
)
def create_review(
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Prevent duplicate reviews
    existing_review = (
        db.query(Review)
        .filter(
            Review.user_id == current_user.id,
            Review.product_id == product_id
        )
        .first()
    )

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product."
        )

    # Create review
    new_review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


# Get Reviews of a Product
@router.get(
    "/products/{product_id}/reviews",
    response_model=list[ReviewResponse]
)
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .all()
    )

    return reviews


# Update Review
@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if review.rating is not None:
        db_review.rating = review.rating

    if review.comment is not None:
        db_review.comment = review.comment

    db.commit()
    db.refresh(db_review)

    return db_review


# Delete Review
@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(db_review)
    db.commit()

    return {
        "message": "Review deleted successfully"
    }