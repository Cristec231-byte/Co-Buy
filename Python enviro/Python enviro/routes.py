from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db import SessionLocal

router = APIRouter()

@router.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
