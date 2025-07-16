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

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        print("🔧 Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create tables on startup: {e}")
        
    # Test database connection
    try:
        if check_database_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")

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
        "tables": "Data table should be auto-created on startup"
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
            "tables": "Data table should be auto-created on startup",
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
    import psutil
    import platform
    
    # Check environment variables
    env_vars = {}
    railway_vars = [
        "DATABASE_URL", "RAILWAY_ENVIRONMENT", "PORT", 
        "RAILWAY_PROJECT_ID", "RAILWAY_SERVICE_ID", "RAILWAY_DEPLOYMENT_ID"
    ]
    
    for var in railway_vars:
        value = os.environ.get(var)
        if var == "DATABASE_URL" and value:
            # Mask password in DATABASE_URL
            env_vars[var] = f"Set (length: {len(value)})"
        else:
            env_vars[var] = value or "Not set"
    
    # Database connection test
    try:
        db_test = check_database_connection()
        db_status = "✅ Connected" if db_test else "❌ Failed"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"
    
    return {
        "system_info": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "working_directory": os.getcwd()
        },
        "environment_variables": env_vars,
        "database_status": db_status,
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "railway_deployment": "Active" if os.environ.get("RAILWAY_ENVIRONMENT") else "Local",
        "message": "Comprehensive Railway deployment diagnostics"
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

# Check table status endpoint
@app.get("/admin/table-status")
def check_table_status(db: Session = Depends(get_db)):
    """Check if tables exist in the database"""
    try:
        from sqlalchemy import text
        
        # Check if data table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        
        data_table_exists = result.scalar()
        
        # Get all tables
        result = db.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        all_tables = [row[0] for row in result.fetchall()]
        
        return {
            "status": "✅ Table status retrieved",
            "data_table_exists": data_table_exists,
            "all_tables": all_tables,
            "table_count": len(all_tables)
        }
    except Exception as e:
        return {
            "status": "❌ Failed to check table status",
            "error": str(e)
        }

# Insert ID "1" into data table
@app.post("/admin/insert-id-1")
def insert_id_1(db: Session = Depends(get_db)):
    """Insert ID '1' into the data table"""
    try:
        print("🔍 Attempting to insert ID 1 into data table...")
        
        # Check if ID 1 already exists
        existing_item = crud.get_data_item(db=db, item_id=1)
        if existing_item:
            print(f"⚠️  ID 1 already exists: {existing_item.id}")
            return {
                "status": "⚠️ ID 1 already exists",
                "message": "Data item with ID 1 already exists in the table",
                "existing_item": {"id": existing_item.id}
            }
        
        print("✅ ID 1 doesn't exist, creating new item...")
        
        # Create new item with ID 1
        new_item = crud.create_data_item_with_id(db=db, item_id=1)
        print(f"✅ Successfully created item with ID: {new_item.id}")
        
        # Verify it was actually inserted
        verify_item = crud.get_data_item(db=db, item_id=1)
        if verify_item:
            print(f"✅ Verification successful: Item with ID {verify_item.id} found")
        else:
            print("❌ Verification failed: Item not found after insertion")
        
        return {
            "status": "✅ ID 1 inserted successfully",
            "message": "Data item with ID 1 created",
            "item": {"id": new_item.id},
            "verification": "Success" if verify_item else "Failed"
        }
    except Exception as e:
        print(f"❌ Error inserting ID 1: {str(e)}")
        return {
            "status": "❌ Failed to insert ID 1",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Direct SQL insert for testing
@app.post("/admin/direct-insert-1")
def direct_insert_id_1(db: Session = Depends(get_db)):
    """Direct SQL insert ID '1' into the data table"""
    try:
        from sqlalchemy import text
        
        print("🔍 Attempting direct SQL insert of ID 1...")
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            return {
                "status": "❌ Table doesn't exist",
                "message": "Data table doesn't exist. Create it first."
            }
        
        # Check if ID 1 already exists
        result = db.execute(text("SELECT COUNT(*) FROM data WHERE id = 1"))
        count = result.scalar()
        
        if count > 0:
            return {
                "status": "⚠️ ID 1 already exists",
                "message": "Data item with ID 1 already exists"
            }
        
        # Direct SQL insert
        db.execute(text("INSERT INTO data (id) VALUES (1)"))
        db.commit()
        
        # Verify insertion
        result = db.execute(text("SELECT id FROM data WHERE id = 1"))
        inserted_id = result.scalar()
        
        print(f"✅ Direct SQL insert successful: ID {inserted_id}")
        
        return {
            "status": "✅ Direct SQL insert successful",
            "message": "ID 1 inserted using direct SQL",
            "inserted_id": inserted_id
        }
        
    except Exception as e:
        print(f"❌ Direct SQL insert failed: {str(e)}")
        return {
            "status": "❌ Direct SQL insert failed",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Insert ID "5" into data table
@app.post("/admin/insert-id-5")
def insert_id_5(db: Session = Depends(get_db)):
    """Insert ID '5' into the data table"""
    try:
        from sqlalchemy import text
        
        print("🔍 Attempting to insert ID 5 into data table...")
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            return {
                "status": "❌ Table doesn't exist",
                "message": "Data table doesn't exist. Create it first with /admin/create-tables"
            }
        
        # Check if ID 5 already exists
        result = db.execute(text("SELECT COUNT(*) FROM data WHERE id = 5"))
        count = result.scalar()
        
        if count > 0:
            return {
                "status": "⚠️ ID 5 already exists",
                "message": "Data item with ID 5 already exists in the table"
            }
        
        # Direct SQL insert of ID 5
        db.execute(text("INSERT INTO data (id) VALUES (5)"))
        db.commit()
        
        # Verify insertion
        result = db.execute(text("SELECT id FROM data WHERE id = 5"))
        inserted_id = result.scalar()
        
        # Get updated count
        result = db.execute(text("SELECT COUNT(*) FROM data"))
        total_count = result.scalar()
        
        print(f"✅ ID 5 inserted successfully: {inserted_id}")
        
        return {
            "status": "✅ ID 5 inserted successfully",
            "message": "Data item with ID 5 created using direct SQL",
            "inserted_id": inserted_id,
            "total_rows": total_count
        }
        
    except Exception as e:
        print(f"❌ Error inserting ID 5: {str(e)}")
        return {
            "status": "❌ Failed to insert ID 5",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Flexible data insertion route
@app.post("/admin/insert-data")
def insert_data(
    id: Optional[int] = None,
    auto_generate: bool = True,
    db: Session = Depends(get_db)
):
    """
    Flexible FastAPI route to insert data into the data table
    
    Parameters:
    - id: Optional specific ID to insert
    - auto_generate: If True, auto-generates ID; if False, requires specific ID
    """
    try:
        from sqlalchemy import text
        
        print(f"🔍 Insert data request - ID: {id}, Auto-generate: {auto_generate}")
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            return {
                "status": "❌ Table doesn't exist",
                "message": "Data table doesn't exist. Create it first with /admin/create-tables"
            }
        
        # Handle different insertion scenarios
        if auto_generate:
            # Auto-generate ID (default behavior)
            result = db.execute(text("INSERT INTO data DEFAULT VALUES RETURNING id"))
            inserted_id = result.scalar()
            db.commit()
            
            print(f"✅ Auto-generated ID: {inserted_id}")
            
            return {
                "status": "✅ Data inserted successfully",
                "message": "Data item created with auto-generated ID",
                "inserted_id": inserted_id,
                "method": "auto_generate"
            }
        
        elif id is not None:
            # Insert specific ID
            # Check if ID already exists
            result = db.execute(text("SELECT COUNT(*) FROM data WHERE id = :id"), {"id": id})
            count = result.scalar()
            
            if count > 0:
                return {
                    "status": "⚠️ ID already exists",
                    "message": f"Data item with ID {id} already exists in the table",
                    "existing_id": id
                }
            
            # Insert specific ID
            db.execute(text("INSERT INTO data (id) VALUES (:id)"), {"id": id})
            db.commit()
            
            print(f"✅ Specific ID inserted: {id}")
            
            return {
                "status": "✅ Data inserted successfully",
                "message": f"Data item created with ID {id}",
                "inserted_id": id,
                "method": "specific_id"
            }
        
        else:
            return {
                "status": "❌ Invalid parameters",
                "message": "Either enable auto_generate or provide a specific ID"
            }
            
    except Exception as e:
        print(f"❌ Error inserting data: {str(e)}")
        return {
            "status": "❌ Failed to insert data",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Bulk data insertion route
@app.post("/admin/bulk-insert")
def bulk_insert_data(
    count: int = 5,
    start_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bulk insert multiple data items
    
    Parameters:
    - count: Number of items to insert (default: 5)
    - start_id: Starting ID for sequential insertion (optional)
    """
    try:
        from sqlalchemy import text
        
        print(f"🔍 Bulk insert request - Count: {count}, Start ID: {start_id}")
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            return {
                "status": "❌ Table doesn't exist",
                "message": "Data table doesn't exist. Create it first with /admin/create-tables"
            }
        
        # Validate count
        if count <= 0 or count > 100:
            return {
                "status": "❌ Invalid count",
                "message": "Count must be between 1 and 100"
            }
        
        inserted_ids = []
        
        if start_id is not None:
            # Insert with sequential IDs
            for i in range(count):
                current_id = start_id + i
                
                # Check if ID already exists
                result = db.execute(text("SELECT COUNT(*) FROM data WHERE id = :id"), {"id": current_id})
                if result.scalar() > 0:
                    print(f"⚠️  ID {current_id} already exists, skipping")
                    continue
                
                # Insert the ID
                db.execute(text("INSERT INTO data (id) VALUES (:id)"), {"id": current_id})
                inserted_ids.append(current_id)
            
            db.commit()
            
        else:
            # Insert with auto-generated IDs
            for i in range(count):
                result = db.execute(text("INSERT INTO data DEFAULT VALUES RETURNING id"))
                inserted_id = result.scalar()
                inserted_ids.append(inserted_id)
            
            db.commit()
        
        print(f"✅ Bulk insert completed: {len(inserted_ids)} items inserted")
        
        return {
            "status": "✅ Bulk insert completed",
            "message": f"Successfully inserted {len(inserted_ids)} data items",
            "inserted_ids": inserted_ids,
            "total_inserted": len(inserted_ids)
        }
        
    except Exception as e:
        print(f"❌ Error in bulk insert: {str(e)}")
        return {
            "status": "❌ Bulk insert failed",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Check what's actually in the data table
@app.get("/admin/inspect-data-table")
def inspect_data_table(db: Session = Depends(get_db)):
    """Inspect the contents of the data table"""
    try:
        from sqlalchemy import text
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'data'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            return {
                "status": "❌ Table doesn't exist",
                "message": "Data table doesn't exist in the database"
            }
        
        # Get table structure
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'data'
            ORDER BY ordinal_position
        """))
        columns = [dict(row._mapping) for row in result.fetchall()]
        
        # Get all data from the table
        result = db.execute(text("SELECT * FROM data"))
        all_data = [dict(row._mapping) for row in result.fetchall()]
        
        # Get row count
        result = db.execute(text("SELECT COUNT(*) FROM data"))
        row_count = result.scalar()
        
        return {
            "status": "✅ Table inspection complete",
            "table_exists": table_exists,
            "table_structure": columns,
            "row_count": row_count,
            "all_data": all_data,
            "message": f"Data table has {row_count} rows"
        }
        
    except Exception as e:
        return {
            "status": "❌ Failed to inspect table",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Data table API endpoints
@app.post("/data/", response_model=schemas.DataResponse)
def create_data_item(data_item: schemas.DataCreate, db: Session = Depends(get_db)):
    """Create a new data item"""
    return crud.create_data_item(db=db, data_item=data_item)

@app.post("/data/insert-id/{item_id}", response_model=schemas.DataResponse)
def create_data_item_with_id(item_id: int, db: Session = Depends(get_db)):
    """Create a data item with a specific ID"""
    try:
        return crud.create_data_item_with_id(db=db, item_id=item_id)
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail=f"Data item with ID {item_id} already exists")
        raise HTTPException(status_code=500, detail=f"Failed to create data item: {str(e)}")

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
