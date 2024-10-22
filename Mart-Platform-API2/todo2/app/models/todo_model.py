# app/models/todo_model.py
from sqlmodel import SQLModel, Field
from typing import  Optional

# class TodoBase(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     content: str = Field(index=True)
#     # title: str = Field(..., max_length=100)
#     # description: str = Field(default=None, max_length=255)
#     # completed: bool = Field(default=False)

# class TodoCreate(TodoBase):
#     pass

# class TodoUpdate(TodoBase):
#     pass

# class TodoDelete(SQLModel):
#     id: int = Field(default=None)
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
