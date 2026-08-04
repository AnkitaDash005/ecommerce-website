from datetime import datetime

from app.auth.dependencies import get_current_user
from app.database import SessionLocal
from app.models.cart import CartItem
from app.models.coupon import Coupon
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.schemas.order import CheckoutRequest, OrderStatusUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/checkout")
def checkout(
    checkout_data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    # Validate stock
    for item in cart_items:
        if item.product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {item.product_id} not found."
            )

        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Only {item.product.stock} item(s) available for "
                    f"'{item.product.name}'."
                )
            )

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    discount = 0

    if checkout_data.coupon:

        coupon = (
            db.query(Coupon)
            .filter(Coupon.code == checkout_data.coupon)
            .first()
        )

        if not coupon:
            raise HTTPException(
                status_code=404,
                detail="Coupon not found"
            )

        if not coupon.is_active:
            raise HTTPException(
                status_code=400,
                detail="Coupon is inactive"
            )

        if coupon.expiry_date < datetime.utcnow():  # noqa: DTZ003
            raise HTTPException(
                status_code=400,
                detail="Coupon has expired"
            )

        if total < coupon.minimum_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Minimum order amount is {coupon.minimum_amount}"
            )

        if coupon.discount_type.lower() == "percentage":
            discount = total * (coupon.discount / 100)

        elif coupon.discount_type.lower() == "flat":
            discount = coupon.discount

        total -= discount

        total = max(total, 0)

    try:
        # Create Order
        order = Order(
            user_id=current_user.id,
            total_price=total,
            status="Pending"
        )

        db.add(order)
        db.flush()

        # Create Order Items and reduce stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )

            db.add(order_item)

            # Reduce stock
            item.product.stock -= item.quantity

        # Clear cart
        for item in cart_items:
            db.delete(item)

        db.commit()
        db.refresh(order)

    except Exception:
        db.rollback()
        raise

    return {
        "order_id": order.id,
        "status": order.status,
        "discount": discount,
        "total_price": order.total_price,
        "items": [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in order.items
        ]
    }


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )

    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in order.items
            ]
        })

    return result


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "status": order.status,
        "total_price": order.total_price,
        "created_at": order.created_at,
        "items": [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in order.items
        ]
    }


@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    # Restore stock
    for item in order.items:
        item.product.stock += item.quantity

    order.status = "Cancelled"

    db.commit()
    db.refresh(order)

    return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "status": order.status
    }

@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    valid_statuses = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "status": order.status
    }