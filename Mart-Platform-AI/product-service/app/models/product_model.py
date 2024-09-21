from sqlmodel import SQLModel, Field, Relationship, HttpUrl
from typing import List, Optional
from app.models.base import BaseIdModel

# ====================== Product Category Model====================
# ====================== Product Category Model====================

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



class Category(BaseIdModel,SQLModel, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    products: List["Product"] = Relationship(back_populates="category") #  1. Relationship with Products

# ====================== Product Model====================
# ====================== Product Model====================


# ====================== Product ProductImage Model====================
# ====================== Product ProductImage Model==================== 

class ProductImage(SQLModel):
    image_url: HttpUrl # As in the Image model we have a url field, we can declare it to be an instance of Pydantic's HttpUrl instead of a str
    name:str
       
    # example product
example_input_prodcut=   {
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


class Product(BaseIdModel,SQLModel, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    name: str = Field(examples=["coca-cola"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35])
    discount_price: float | None = Field(default=None, examples=[3.2])
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    stock: int = Field(default=0)
    images: list[ProductImage] | None = None
    tags: set[str] = set()   # list of unique tags using set() ,to avoid duplicates we cannot use this list "tags: List[str] = []"
    is_active: bool = Field(default=True)
    category_id: int | None = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    rating: List["ProductRating"] = Relationship(back_populates="product")


    
    # rating: list["ProductRating"] = Relationship(back_populates="product")
    # image: str # Multiple | URL Not Media | One to Manu Relationship
    # quantity: int | None = None # Shall it be managed by Inventory Microservice
    # color: str | None = None # One to Manu Relationship
    # rating: float | None = None # One to Manu Relationship
    
 
# ====================== Product ProductRating Model====================
# ====================== Product ProductRating Model====================  

class ProductRating(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    user_id: int  # Assuming you have a User Service
    rating: int  # Rating from 1 to 5
    review: str | None = None
    product: Product = Relationship(back_populates="rating")
    
    # user_id: int # One to Manu Relationship
   
   
   
   

# =========================Product Update Model=========================
# =========================Product Update Model=========================

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    discount_price: float | None = None
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    category: str | None = None
    stock: int | None = None
    is_active: bool | None = None
    category_id: int | None= None