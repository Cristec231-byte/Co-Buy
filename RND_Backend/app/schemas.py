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

# Journal schemas
class JournalBase(BaseModel):
    journal_number: str
    last_loaded: Optional[datetime] = None
    file_type: str = "CSV"

class JournalCreate(JournalBase):
    pass

class JournalUpdate(BaseModel):
    last_loaded: Optional[datetime] = None
    file_type: Optional[str] = None
    # Note: journal_number is not included since it's the primary key

class Journal(JournalBase):
    updated: datetime

    class Config:
        from_attributes = True
