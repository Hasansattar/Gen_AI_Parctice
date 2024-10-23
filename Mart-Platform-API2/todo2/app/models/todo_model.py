# app/models/todo_model.py
from sqlmodel import SQLModel, Field
from typing import  Optional


class TodoBase(SQLModel):
    title: str = Field(..., max_length=100)
    description: str = Field(default=None, max_length=255)
    completed: bool = Field(default=False)

class TodoCreate(TodoBase,table=True):
     id: Optional[int] = Field(default=None, primary_key=True) 


class Todo(TodoBase):
     id: Optional[int] = Field(default=None, primary_key=True) 


class TodoUpdate(TodoBase):
    pass




    
        