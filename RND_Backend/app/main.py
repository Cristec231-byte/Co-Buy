from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

import models, schemas, crud
from database import SessionLocal, engine, init_db

# Initialize database with force creation
print("🔄 Initializing database...")
if init_db():
    print("✅ Database initialization complete - Tables: items, investors")
else:
    print("❌ Database initialization failed")

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

# Test database connection
@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    """Test PostgreSQL connection and show table info"""
    try:
        # Count items and investors
        item_count = db.query(models.Item).count()
        investor_count = db.query(models.Investor).count()
        
        return {
            "status": "✅ PostgreSQL connection successful",
            "database": "Railway PostgreSQL",
            "tables": {
                "items": item_count,
                "investors": investor_count
            },
            "message": "Database is working correctly!"
        }
    except Exception as e:
        return {
            "status": "❌ Database connection failed",
            "error": str(e)
        }

# ===================
# ITEM ENDPOINTS
# ===================

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
    updated_item = crud.update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db, item_id)

# ===================
# INVESTOR ENDPOINTS
# ===================

@app.post("/investors/", response_model=schemas.Investor)
def create_investor(investor: schemas.InvestorCreate, db: Session = Depends(get_db)):
    """Create a new investor"""
    # Check if email already exists
    db_investor = crud.get_investor_by_email(db, email=investor.email)
    if db_investor:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_investor(db, investor)

@app.get("/investors/", response_model=List[schemas.Investor])
def read_investors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all investors with pagination"""
    return crud.get_investors(db, skip=skip, limit=limit)

@app.get("/investors/search", response_model=List[schemas.Investor])
def search_investors(
    q: str = Query(..., description="Search term for name or email"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Search investors by name or email"""
    return crud.search_investors(db, search_term=q, skip=skip, limit=limit)

@app.get("/investors/{investor_id}", response_model=schemas.Investor)
def read_investor(investor_id: int, db: Session = Depends(get_db)):
    """Get a specific investor by ID"""
    db_investor = crud.get_investor(db, investor_id)
    if db_investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    return db_investor

@app.put("/investors/{investor_id}", response_model=schemas.Investor)
def update_investor(investor_id: int, investor: schemas.InvestorUpdate, db: Session = Depends(get_db)):
    """Update an investor"""
    # If email is being updated, check it doesn't already exist
    if investor.email:
        existing_investor = crud.get_investor_by_email(db, email=investor.email)
        if existing_investor and existing_investor.id != investor_id:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    updated_investor = crud.update_investor(db, investor_id, investor)
    if updated_investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    return updated_investor

@app.delete("/investors/{investor_id}")
def delete_investor(investor_id: int, db: Session = Depends(get_db)):
    """Delete an investor"""
    return crud.delete_investor(db, investor_id)

# ===================
# DATABASE MANAGEMENT
# ===================

@app.post("/reset-db")
def reset_database(db: Session = Depends(get_db)):
    """Force recreate all database tables - USE WITH CAUTION!"""
    try:
        # Drop all existing tables
        models.Base.metadata.drop_all(bind=engine)
        # Create all tables fresh
        models.Base.metadata.create_all(bind=engine)
        
        return {
            "status": "✅ Database reset successful",
            "message": "All tables recreated including investors table",
            "tables": ["items", "investors"]
        }
    except Exception as e:
        return {
            "status": "❌ Database reset failed",
            "error": str(e)
        }
