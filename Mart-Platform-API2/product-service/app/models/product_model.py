from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
from typing import List, Optional
from app.models.base import BaseIdModel

# ====================== Product Category Model ====================
# ====================== Product Category Model ====================

# Response Model examples
example_input_uni = {
    "name": "T-shirt",
    "description": "new T-shirt collection in pakistan.",
}

example_output_uni = {
    "id": 1,
    "name": "University of PIAIC",
    "description": "The University of PIAIC is a leading educational institution in Pakistan.",
}

class Category(BaseIdModel, SQLModel, table=True):
    name: str
    description: Optional[str] = None
    products: List["Product"] = Relationship(back_populates="category")  # 1. Relationship with Products


# ====================== Product ProductImage Model ====================
# ====================== Product ProductImage Model ====================

class ProductImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image_url: str
    name: str
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="images")


# ====================== Product Model ====================
# ====================== Product Model ====================

example_input_product = {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}

class Product(BaseIdModel, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: float = Field(default=None)
    discount_price: Optional[float] = Field(default=None)
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    stock: int = Field(default=0)
    
    # # Using JSON to store list of ProductImage objects
    # images: Optional[List[ProductImage]] = Field(sa_column=JSON)  
    
    # # Using JSON to store a list of tags
    # tags: Optional[List[str]] = Field(default=[], sa_column=JSON)
    
    images: List[ProductImage] = Relationship(back_populates="product")
    tags: str | None = None  # store tags as a comma-separated string
    
    is_active: bool = Field(default=True)
    category_id: Optional[int] = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    
    # Relationship with ProductRating
    rating: List["ProductRating"] = Relationship(back_populates="product")


# ====================== Product ProductRating Model ====================
# ====================== Product ProductRating Model ====================

class ProductRating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    user_id: int  # Assuming you have a User Service
    rating: int  # Rating from 1 to 5
    review: Optional[str] = None
    product: Product = Relationship(back_populates="rating")


# ========================= Product Update Model =========================
# ========================= Product Update Model =========================

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None