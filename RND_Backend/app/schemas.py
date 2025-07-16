from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Pydantic schemas for Data table
class DataBase(BaseModel):
    pass

class DataCreate(DataBase):
    pass

class DataResponse(DataBase):
    id: int
    
    class Config:
        from_attributes = True
