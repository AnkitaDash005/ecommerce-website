from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.database import Base, engine

# Import models (needed for SQLAlchemy table creation)
from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.models.category import Category
from app.models.coupon import Coupon
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.reviews import Review
from app.models.wishlist import Wishlist

# Import routers
from app.routers import categories
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.coupons import router as coupon_router
from app.routers.orders import router as order_router
from app.routers.products import router as product_router
from app.routers.wishlist import router as wishlist_router
from app.routers.review import router as review_router



# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
)


# CORS Middleware (Frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(categories.router)
app.include_router(wishlist_router)
app.include_router(coupon_router)
app.include_router(review_router)



@app.get("/")
def home():
    return {
        "message": "Welcome to E-Commerce API"
    }


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )