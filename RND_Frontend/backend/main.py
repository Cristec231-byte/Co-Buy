# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import os

# -------------------
# Load Environment
# -------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")
TABLE_NAME = os.getenv("TABLE_NAME", "Users")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE")

# Supabase client (shared)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# -------------------
# App Setup
# -------------------
app = FastAPI(
    title="Co-Buy Backend",
    description="FastAPI backend for authentication and property management",
    version="1.0.0",
)

# Enable CORS for frontend (Vite defaults to :5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # in case you use CRA
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Routers
# -------------------
from auth import router as auth_router   # ✅ import auth router
from users import router as users_router

app.include_router(auth_router, prefix="/auth", tags=["Auth"])  # ✅ include auth router
app.include_router(users_router, prefix="/users", tags=["Users"])

# -------------------
# Health Check
# -------------------
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
