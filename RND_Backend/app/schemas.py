from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Pydantic schemas for Test table
class TestTableBase(BaseModel):
    name: str
    description: Optional[str] = None

class TestTableCreate(TestTableBase):
    pass

class TestTableUpdate(TestTableBase):
    name: Optional[str] = None

class TestTableResponse(TestTableBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
