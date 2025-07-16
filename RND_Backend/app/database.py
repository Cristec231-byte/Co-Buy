from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Railway's DATABASE_URL environment variable, fallback to local
DATABASE_URL = os.environ.get("DATABASE_URL")

# Handle empty or missing DATABASE_URL
if not DATABASE_URL or DATABASE_URL.strip() == "":
    # Fallback to Railway internal connection
    DATABASE_URL = "postgresql://postgres:pPhqSquMxbQSnkoljCvXPAMoOJnHFFyB@postgres.railway.internal:5432/railway"
    print("⚠️  No DATABASE_URL found, using Railway internal connection")
else:
    print(f"🔗 Using DATABASE_URL: {DATABASE_URL[:50]}...")

# Railway provides DATABASE_URL in postgres:// format, but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Railway internal connections don't need SSL
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={"sslmode": "disable"}
    )
    print("✅ Database engine created successfully")
except Exception as e:
    print(f"❌ Failed to create database engine: {e}")
    # Create a dummy engine to prevent app crash
    engine = create_engine("sqlite:///./temp.db")
    print("⚠️  Using temporary SQLite database")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def check_database_connection():
    """Check if database connection is working"""
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
