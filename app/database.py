from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Railway's DATABASE_URL environment variable, fallback to local
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:cobuy@localhost/Cobuy")

# Railway provides DATABASE_URL in postgres:// format, but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Add SSL configuration for Railway
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"} if "railway" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def init_db():
    """Initialize database - create all tables"""
    import models  # Import here to avoid circular imports
    try:
        # Force create all tables
        models.Base.metadata.create_all(bind=engine)
        print("✅ All database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
