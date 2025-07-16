#!/usr/bin/env python3
"""
Railway startup script for Co-Buy backend
Handles environment validation and database connection
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate Railway environment variables"""
    logger.info("🚀 Starting Co-Buy backend on Railway...")
    
    # Check environment variables
    database_url = os.environ.get("DATABASE_URL", "")
    port = os.environ.get("PORT", "8000")
    railway_env = os.environ.get("RAILWAY_ENVIRONMENT", "unknown")
    
    logger.info(f"📊 Railway Environment: {railway_env}")
    logger.info(f"🔌 Port: {port}")
    logger.info(f"🗄️  Database URL: {'✅ Set' if database_url else '❌ Empty'}")
    
    if not database_url:
        logger.warning("⚠️  DATABASE_URL is empty - using fallback connection")
        # Set fallback DATABASE_URL for Railway internal PostgreSQL
        fallback_url = "postgresql://postgres:pPhqSquMxbQSnkoljCvXPAMoOJnHFFyB@postgres.railway.internal:5432/railway"
        os.environ["DATABASE_URL"] = fallback_url
        logger.info("🔄 Set fallback DATABASE_URL for Railway PostgreSQL")
    
    return port

def main():
    """Main startup function"""
    try:
        port = validate_environment()
        
        # Import and run the FastAPI app
        logger.info("📦 Loading FastAPI application...")
        import uvicorn
        from main import app
        
        logger.info(f"🌐 Starting server on port {port}")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(port),
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
