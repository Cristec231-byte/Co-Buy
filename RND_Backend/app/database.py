from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Railway's DATABASE_URL environment variable, fallback to local
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:pPhqSquMxbQSnkoljCvXPAMoOJnHFFyB@postgres.railway.internal:5432/railway")

# Railway provides DATABASE_URL in postgres:// format, but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Railway internal connections don't need SSL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "disable"}
)

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
