from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartCreate, CartUpdate
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/")
def add_to_cart(
    cart: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == cart.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the product is already in the user's cart
    existing_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == cart.product_id
        )
        .first()
    )

    # If it exists, increase the quantity
    if existing_item:
        existing_item.quantity += cart.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    # Otherwise, create a new cart item
    cart_item = CartItem(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .all()
    )

    total = 0
    items = []

    for item in cart:
        subtotal = float(item.product.price) * item.quantity
        total += subtotal

        items.append({
            "id": item.id,
            "product": item.product.name,
            "quantity": item.quantity,
            "price": float(item.product.price),
            "subtotal": subtotal
        })

    return {
        "items": items,
        "total": total
    }

@router.put("/{cart_id}")
def update_cart(
    cart_id: int,
    item: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_id,
            CartItem.user_id == current_user.id
        )
        .first()
    )

    if not cart:
        raise HTTPException(status_code=404, detail="Item not found")

    cart.quantity = item.quantity

    db.commit()
    db.refresh(cart)

    return cart

@router.delete("/{cart_id}")
def delete_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_id,
            CartItem.user_id == current_user.id
        )
        .first()
    )

    if not cart:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(cart)
    db.commit()

    return {"message": "Item removed"}
