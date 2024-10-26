from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ================================================================
# Order Base Model
# ================================================================

class OrderBase(SQLModel):
    user_id: int = Field(index=True)  # Link to User ID
    status: str = Field(default="pending", max_length=20)  # Order status: pending, confirmed, etc.
    total_amount: float = Field(..., gt=0)  # Total cost must be greater than 0
    payment_status: str = Field(default="unpaid", max_length=20)  # Payment status: unpaid, paid, failed
    shipping_address: str = Field(max_length=255)
    order_date: datetime = Field(default=datetime.utcnow)


class OrderCreate(OrderBase, table=True):  # Create table in DB
    id: Optional[int] = Field(default=None, primary_key=True)
    items: List["OrderItemCreate"] = Relationship(back_populates="order")  # Link to OrderItemCreate
    payments: List["PaymentCreate"] = Relationship(back_populates="order")  # Link to PaymentCreate
    status_history: List["OrderStatusHistoryCreate"] = Relationship(back_populates="order")  # Link to OrderStatusHistoryCreate


class Order(OrderBase):  # Read model
    id: Optional[int] = Field(default=None, primary_key=True)
    items: List["OrderItem"] = Relationship(back_populates="order")  # Link to OrderItem
    payments: List["Payment"] = Relationship(back_populates="order")  # Link to Payment
    status_history: List["OrderStatusHistory"] = Relationship(back_populates="order")  # Link to OrderStatusHistory


class OrderUpdate(SQLModel):  # Update model
    status: Optional[str] = Field(default=None, max_length=20)
    payment_status: Optional[str] = Field(default=None, max_length=20)
    shipping_address: Optional[str] = Field(default=None, max_length=255)


# ================================================================
# Order Item Model
# ================================================================

class OrderItemBase(SQLModel):
    product_id: int = Field(index=True)  # Link to Product ID
    quantity: int = Field(..., ge=1)  # Quantity ordered must be 1 or more
    price_per_unit: float = Field(..., gt=0)  # Unit price must be greater than 0
    total_price: float = Field(..., gt=0)  # Calculated total (quantity * price_per_unit)


class OrderItemCreate(OrderItemBase, table=True):  # Create table in DB
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int  = Field(foreign_key="ordercreate.id")  # Link to OrderCreate
    order: Optional[OrderCreate] = Relationship(back_populates="items")  # Back-populate relationship with OrderCreate


class OrderItem(OrderItemBase):  # Read model
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int  = Field(foreign_key="order.id")  # Link to Order
    order: Optional[Order] = Relationship(back_populates="items")  # Back-populate relationship with Order


class OrderItemUpdate(SQLModel):  # Update model
    quantity: Optional[int] = Field(default=None, ge=1)
    price_per_unit: Optional[float] = Field(default=None, gt=0)
    total_price: Optional[float] = Field(default=None, gt=0)


# ================================================================
# Payment Model
# ================================================================

class PaymentBase(SQLModel):
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., max_length=50)  # Payment method, e.g., card, PayPal, etc.
    status: str = Field(default="pending", max_length=20)  # Payment status: pending, completed, failed
    transaction_id: Optional[str] = Field(default=None, max_length=50)  # External transaction ID, if available


class PaymentCreate(PaymentBase, table=True):  # Create table in DB
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="ordercreate.id")  # Link to OrderCreate
    order: Optional[OrderCreate] = Relationship(back_populates="payments")  # Link to OrderCreate


class Payment(PaymentBase):  # Read model
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")  # Link to Order
    order: Optional[Order] = Relationship(back_populates="payments")  # Link to Order


class PaymentUpdate(SQLModel):  # Update model
    status: Optional[str] = Field(default=None, max_length=20)
    transaction_id: Optional[str] = Field(default=None, max_length=50)


# ================================================================
# Order Status History Model
# ================================================================

class OrderStatusHistoryBase(SQLModel):
    status: str = Field(..., max_length=20)  # Order status at this point in time
    timestamp: datetime = Field(default=datetime.utcnow)


class OrderStatusHistoryCreate(OrderStatusHistoryBase, table=True):  # Create table in DB
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="ordercreate.id")  # Link to OrderCreate
    order: Optional[OrderCreate] = Relationship(back_populates="status_history")  # Link to OrderCreate


class OrderStatusHistory(OrderStatusHistoryBase):  # Read model
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")  # Link to Order
    order: Optional[Order] = Relationship(back_populates="status_history")  # Link to Order


