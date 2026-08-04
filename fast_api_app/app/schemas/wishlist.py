from pydantic import BaseModel


class ProductMini(BaseModel):
    name: str
    price: float

    class Config:
        from_attributes = True



class WishlistCreate(BaseModel):
    product_id: int



class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: ProductMini

    class Config:
        from_attributes = True