from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    file_type = Column(String, nullable=True)


