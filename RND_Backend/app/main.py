from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

import models, schemas, crud
from database import SessionLocal, engine, check_database_connection

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
    db_status = "healthy" if check_database_connection() else "unhealthy"
    return {
        "status": "healthy", 
        "message": "Co-Buy API is running",
        "database": db_status,
        "tables": "All tables removed - clean database"
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
            "tables": "All tables removed - clean database",
            "message": "Database connection is working correctly!"
        }
    except Exception as e:
        return {
            "status": "❌ Database connection failed",
            "error": str(e)
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
