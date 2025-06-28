from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Railway's DATABASE_URL environment variable, fallback to local
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:cobuy@localhost/Cobuy")

# Railway provides DATABASE_URL in postgres:// format, but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
