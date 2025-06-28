import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the FastAPI app
from main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Fixed: 8000 is correct for web server, not 5432
    uvicorn.run(app, host="0.0.0.0", port=port)
