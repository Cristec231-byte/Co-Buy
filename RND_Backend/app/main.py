from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

import models, schemas, crud
from database import SessionLocal, engine, check_database_connection

# Print startup information
print("🚀 Starting Co-Buy API...")
print(f"📊 Database URL set: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}")
print(f"🌍 Railway Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'Not set')}")

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
    try:
        db_status = "healthy" if check_database_connection() else "unhealthy"
        database_info = f"Database: {db_status}"
    except Exception as e:
        db_status = "error"
        database_info = f"Database error: {str(e)}"
    
    return {
        "status": "healthy", 
        "message": "Co-Buy API is running",
        "database": db_status,
        "database_info": database_info,
        "tables": "Data table available - use /admin/create-tables to create"
    }

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
@app.get("/test-db")
def test_database_connection_endpoint(db: Session = Depends(get_db)):
    """Test PostgreSQL connection"""
    try:
        from sqlalchemy import text
        result = db.execute(text("SELECT version()"))
        pg_version = result.scalar()
        
        return {
            "status": "✅ PostgreSQL connection successful",
            "database": "Railway PostgreSQL",
            "postgresql_version": pg_version,
            "tables": "Data table available - use /admin/create-tables to create",
            "message": "Database connection is working correctly!"
        }
    except Exception as e:
        return {
            "status": "❌ Database connection failed",
            "error": str(e)
        }

# Debug endpoint for Railway deployment
@app.get("/debug")
def debug_info():
    """Debug information for Railway deployment"""
    return {
        "environment_variables": {
            "DATABASE_URL": "Set" if os.environ.get("DATABASE_URL") else "Not set",
            "RAILWAY_ENVIRONMENT": os.environ.get("RAILWAY_ENVIRONMENT", "Not set"),
            "PORT": os.environ.get("PORT", "Not set")
        },
        "database_url_length": len(os.environ.get("DATABASE_URL", "")),
        "python_path": os.getcwd(),
        "message": "Debug info for Railway deployment"
    }

# Drop all tables endpoint
@app.post("/admin/drop-all-tables")
def drop_all_tables(db: Session = Depends(get_db)):
    """Drop all existing tables"""
    try:
        from sqlalchemy import text
        
        # Get all table names
        result = db.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        
        # Drop each table
        for table in tables:
            db.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        
        db.commit()
        
        return {
            "status": "✅ All tables dropped successfully",
            "message": f"Dropped {len(tables)} tables",
            "tables_dropped": tables
        }
    except Exception as e:
        return {
            "status": "❌ Failed to drop tables",
            "error": str(e)
        }

# Create tables endpoint
@app.post("/admin/create-tables")
def create_tables():
    """Create all tables"""
    try:
        models.Base.metadata.create_all(bind=engine)
        return {
            "status": "✅ Tables created successfully",
            "message": "Data table created",
            "tables": ["data"]
        }
    except Exception as e:
        return {
            "status": "❌ Failed to create tables",
            "error": str(e)
        }

# Data table API endpoints
@app.post("/data/", response_model=schemas.DataResponse)
def create_data_item(data_item: schemas.DataCreate, db: Session = Depends(get_db)):
    """Create a new data item"""
    return crud.create_data_item(db=db, data_item=data_item)

@app.get("/data/", response_model=List[schemas.DataResponse])
def read_data_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all data items"""
    return crud.get_data_items(db=db, skip=skip, limit=limit)

@app.get("/data/{item_id}", response_model=schemas.DataResponse)
def read_data_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific data item"""
    db_item = crud.get_data_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Data item not found")
    return db_item

@app.delete("/data/{item_id}")
def delete_data_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a data item"""
    db_item = crud.delete_data_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Data item not found")
    return {"message": "Data item deleted successfully"}
    return {"message": "Test item deleted successfully"}
