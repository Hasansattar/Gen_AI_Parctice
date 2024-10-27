from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# =========================== USER MODEL ==========================

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    phone: Optional[str] = None
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    role: str = Field(default="Customer")  # e.g., "Customer", "Admin"

class User(UserBase):  # No table=True here
    # This model is only for shared attributes and does not create a database table
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    profile: Optional["UserProfile"] = Relationship(back_populates="user")
    events: List["UserEvent"] = Relationship(back_populates="user")
    

class UserCreate(UserBase, table=True):  # Only this will create a table
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    profile: Optional["UserProfile"] = Relationship(back_populates="user", sa_relationship_kwargs={"primaryjoin": "UserCreate.id == UserProfile.user_id"})
    events: List["UserEvent"] = Relationship(back_populates="user", sa_relationship_kwargs={"primaryjoin": "UserCreate.id == UserEvent.user_id"})

class UserUpdate(SQLModel):
    password_hash: str = Field(nullable=False)
    phone: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# =========================== USER PROFILE MODEL ==========================

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    user_id: int = Field(foreign_key="usercreate.id")  # Use UserCreate table name

    # Relationships
    user: UserCreate = Relationship(back_populates="profile")

# =========================== AUTH MODELS ==========================

class UserLoginRequest(SQLModel):
    username: str
    password: str

class UserLoginResponse(SQLModel):
    user_id: int
    access_token: str
    refresh_token: str

class PasswordResetRequest(SQLModel):
    username: str
    oldpassword: str
    newpassword: str

# class PasswordResetConfirm(SQLModel):
#     reset_token: str
#     new_password: str

# =========================== USER EVENT MODEL ==========================

class UserEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str  # e.g., "CREATED", "UPDATED", "DELETED", "VERIFIED"
    event_payload: Optional[str] = None  # JSON-encoded user data
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    user_id: int = Field(foreign_key="usercreate.id")  # Use UserCreate table name

    # Relationships
    user: UserCreate = Relationship(back_populates="events")
