from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Data schemas for testing PostgreSQL
class DataBase(BaseModel):
    title: str
    content: Optional[str] = None
    status: Optional[str] = "active"

class DataCreate(DataBase):
    pass

class DataUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None

class Data(DataBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
