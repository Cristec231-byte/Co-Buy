from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

import models, schemas, crud  

from database import SessionLocal, engine

# Create all tables (including the new 'data' table)
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully - Tables: items, data")
except Exception as e:
    print(f"❌ Database table creation failed: {e}")

# Create FastAPI app
app = FastAPI(title="Co-Buy API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Co-Buy API is running"}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db, item_id)

# Data endpoints for testing PostgreSQL
@app.post("/data/", response_model=schemas.Data)
def create_data_entry(data: schemas.DataCreate, db: Session = Depends(get_db)):
    """Create a new data entry to test PostgreSQL connection"""
    return crud.create_data_entry(db, data)

@app.get("/data/", response_model=List[schemas.Data])
def read_data_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all data entries"""
    return crud.get_data_entries(db, skip=skip, limit=limit)

@app.get("/data/{data_id}", response_model=schemas.Data)
def read_data_entry(data_id: int, db: Session = Depends(get_db)):
    """Get a specific data entry"""
    db_data = crud.get_data_entry(db, data_id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return db_data

@app.put("/data/{data_id}", response_model=schemas.Data)
def update_data_entry(data_id: int, data: schemas.DataUpdate, db: Session = Depends(get_db)):
    """Update a data entry"""
    db_data = crud.update_data_entry(db, data_id, data)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return db_data

@app.delete("/data/{data_id}")
def delete_data_entry(data_id: int, db: Session = Depends(get_db)):
    """Delete a data entry"""
    result = crud.delete_data_entry(db, data_id)
    if not result.get("deleted"):
        raise HTTPException(status_code=404, detail="Data entry not found")
    return result

# Database test endpoint
@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    """Test PostgreSQL connection and show table info"""
    try:
        # Test basic query
        data_count = db.query(models.Data).count()
        items_count = db.query(models.Item).count()
        
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        
        return {
            "status": "success",
            "message": "PostgreSQL connection working!",
            "tables": {
                "data": f"{data_count} entries",
                "items": f"{items_count} entries"
            },
            "database_url": "Connected to Railway PostgreSQL" if "railway" in str(db.bind.url).lower() else "Connected to local database"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
