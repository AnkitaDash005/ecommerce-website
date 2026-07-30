from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartCreate, CartUpdate

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_to_cart(item: CartCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = CartItem(
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/")
def view_cart(db: Session = Depends(get_db)):
    cart = db.query(CartItem).all()

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
def update_cart(cart_id: int, item: CartUpdate, db: Session = Depends(get_db)):
    cart = db.query(CartItem).filter(CartItem.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Item not found")

    cart.quantity = item.quantity

    db.commit()
    db.refresh(cart)

    return cart


@router.delete("/{cart_id}")
def delete_item(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(CartItem).filter(CartItem.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(cart)
    db.commit()

    return {"message": "Item removed"}