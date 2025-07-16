from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

# Simple data table with just ID
class Data(Base):
    __tablename__ = "data"
    
    id = Column(Integer, primary_key=True, index=True)