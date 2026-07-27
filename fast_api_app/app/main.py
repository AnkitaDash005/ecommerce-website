from fastapi import FastAPI

from app.routers.products import router as product_router

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)

app.include_router(product_router)


@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce API"}