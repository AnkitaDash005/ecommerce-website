from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product as ProductModel
from app.models.reviews import Review
from app.schemas.pagination import ProductPagination
from app.schemas.product import (
    Product,
    ProductCreate,
    StockUpdate,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create Product
@router.post("/", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = ProductModel(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image=product.image,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    avg_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.product_id == new_product.id)
        .scalar()
    )

    new_product.average_rating = (
        round(avg_rating, 1)
        if avg_rating is not None
        else None
    )

    return new_product


# Get All Products
@router.get("/", response_model=ProductPagination)
def get_products(
    page: int = 1,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    category_id: int | None = None,
    in_stock: bool | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductModel)

    if min_price is not None:
        query = query.filter(ProductModel.price >= min_price)

    if max_price is not None:
        query = query.filter(ProductModel.price <= max_price)

    if category_id is not None:
        query = query.filter(ProductModel.category_id == category_id)

    if in_stock:
        query = query.filter(ProductModel.stock > 0)

    if sort == "price":
        query = query.order_by(ProductModel.price.asc())

    elif sort == "-price":
        query = query.order_by(ProductModel.price.desc())

    elif sort == "name":
        query = query.order_by(ProductModel.name.asc())

    elif sort == "latest":
        query = query.order_by(ProductModel.id.desc())

    total = query.count()

    products = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    for product in products:
        avg_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.product_id == product.id)
            .scalar()
        )

        product.average_rating = (
            round(avg_rating, 1)
            if avg_rating is not None
            else None
        )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "products": products
    }


# Search Products
@router.get("/search", response_model=list[Product])
def search_products(
    name: str | None = None,
    description: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductModel)

    if name:
        query = query.filter(
            ProductModel.name.ilike(f"%{name}%")
        )

    if description:
        query = query.filter(
            ProductModel.description.ilike(f"%{description}%")
        )

    products = query.all()

    for product in products:
        avg_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.product_id == product.id)
            .scalar()
        )

        product.average_rating = (
            round(avg_rating, 1)
            if avg_rating is not None
            else None
        )

    return products


# Low Stock Products
@router.get("/low-stock", response_model=list[Product])
def get_low_stock_products(
    threshold: int = 5,
    db: Session = Depends(get_db)
):
    products = (
        db.query(ProductModel)
        .filter(ProductModel.stock < threshold)
        .all()
    )

    for product in products:
        avg_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.product_id == product.id)
            .scalar()
        )

        product.average_rating = (
            round(avg_rating, 1)
            if avg_rating is not None
            else None
        )

    return products


# Get Product By ID
@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    avg_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.product_id == product.id)
        .scalar()
    )

    product.average_rating = (
        round(avg_rating, 1)
        if avg_rating is not None
        else None
    )

    return product


# Update Product Stock
@router.patch("/{product_id}/stock")
def update_stock(
    product_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.stock = stock_data.stock

    db.commit()
    db.refresh(product)

    return {
        "message": "Stock updated successfully",
        "product_id": product.id,
        "stock": product.stock
    }