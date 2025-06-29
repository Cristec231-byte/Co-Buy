from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Item schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# Investor schemas
class InvestorBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: EmailStr
    file_type: Optional[str] = None

class InvestorCreate(InvestorBase):
    pass

class InvestorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    file_type: Optional[str] = None

class Investor(InvestorBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

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
