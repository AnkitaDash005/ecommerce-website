from app.auth.dependencies import get_current_user
from app.database import SessionLocal
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.models.wishlist import Wishlist
from app.schemas.wishlist import (
    WishlistCreate,
    WishlistResponse,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add product to wishlist
@router.post(
    "/",
    response_model=WishlistResponse,
    status_code=status.HTTP_201_CREATED
)
def add_to_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = (
        db.query(Product)
        .filter(Product.id == wishlist.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_item = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == wishlist.product_id
        )
        .first()
    )

    if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Product already in wishlist"
        )

    new_item = Wishlist(
        user_id=current_user.id,
        product_id=wishlist.product_id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# Get current user's wishlist
@router.get(
    "/",
    response_model=list[WishlistResponse]
)
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id)
        .all()
    )


# Delete wishlist item
@router.delete("/{wishlist_id}")
def delete_wishlist_item(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = (
        db.query(Wishlist)
        .filter(
            Wishlist.id == wishlist_id,
            Wishlist.user_id == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Wishlist item removed successfully"
    }


# Move wishlist item to cart
@router.post("/{wishlist_id}/move-to-cart")
def move_to_cart(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    wishlist_item = (
        db.query(Wishlist)
        .filter(
            Wishlist.id == wishlist_id,
            Wishlist.user_id == current_user.id
        )
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == wishlist_item.product_id
        )
        .first()
    )

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=wishlist_item.product_id,
            quantity=1
        )
        db.add(cart_item)

    db.delete(wishlist_item)
    db.commit()

    return {
        "message": "Product moved to cart successfully"
    }