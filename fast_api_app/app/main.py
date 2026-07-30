from fastapi import FastAPI
from app.database import Base, engine
from scalar_fastapi import get_scalar_api_reference
from app.routers.products import router as product_router
from app.routers.cart import router as cart_router

from app.models.product import Product
from app.models.cart import CartItem



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
)

app.include_router(product_router)
app.include_router(cart_router)


@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce API"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

