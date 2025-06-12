# main.py

from fastapi import FastAPI
from db import engine
from models import Base  # Base comes from models/__init__.py

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI + PostgreSQL is working!"}
