from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")
TABLE_NAME = os.getenv("TABLE_NAME", "Users")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE")

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
app = FastAPI()

# Models
class User(BaseModel):
    Email: EmailStr
    Name: str
    Role: str = "user"  # default role

class MagicLinkRequest(BaseModel):
    Email: EmailStr

# Test route
@app.get("/")
def root():
    return {"message": "Backend is running!"}

# -------------------
# CRUD
# -------------------
@app.post("/users")
def create_user(user: User):
    try:
        # 1️⃣ Get current max Investor_id
        max_id_resp = supabase.table(TABLE_NAME).select("Investor_id").order("Investor_id", desc=True).limit(1).execute()
        next_id = 1
        if max_id_resp.data and len(max_id_resp.data) > 0 and max_id_resp.data[0].get("Investor_id") is not None:
            next_id = int(max_id_resp.data[0]["Investor_id"]) + 1

        # 2️⃣ Prepare data (match your table exactly)
        insert_data = {
            "Investor_id": next_id,
            "Email": user.Email,   # Make sure your table column is exactly "Email"
            "Name": user.Name      # Make sure your table column is exactly "Name"
        }

        # Add Role only if your table has it
        try:
            sample_row = supabase.table(TABLE_NAME).select("*").limit(1).execute().data
            if sample_row and "Role" in sample_row[0]:
                insert_data["Role"] = user.Role
        except:
            pass  # ignore if Role column doesn't exist

        # 3️⃣ Insert
        result = supabase.table(TABLE_NAME).insert(insert_data).execute()
        if hasattr(result, "error") and result.error:
            raise HTTPException(status_code=400, detail=str(result.error))
        return result.data

    except Exception as e:
        # Catch all errors and return them clearly
        raise HTTPException(status_code=500, detail=f"Create user failed: {e}")


@app.get("/users")
def get_users():
    result = supabase.table(TABLE_NAME).select("*").execute()
    return result.data

@app.put("/users/{investor_id}")
def update_user(investor_id: str, user: User):
    result = supabase.table(TABLE_NAME).update({
        "Email": user.Email,
        "Name": user.Name,
        "Role": user.Role
    }).eq("Investor_id", investor_id).execute()

    if hasattr(result, "error") and result.error:
        raise HTTPException(status_code=400, detail=str(result.error))
    return result.data

@app.delete("/users/{investor_id}")
def delete_user(investor_id: str):
    result = supabase.table(TABLE_NAME).delete().eq("Investor_id", investor_id).execute()
    if hasattr(result, "error") and result.error:
        raise HTTPException(status_code=400, detail=str(result.error))
    return {"message": "User deleted"}

# -------------------
# MAGIC LINK
# -------------------
@app.post("/request-magic-link")
def request_magic_link(data: MagicLinkRequest):
    email = data.Email

    # Ensure user exists
    existing = supabase.table(TABLE_NAME).select("*").eq("Email", email).execute()
    if not existing.data:
        new_user = supabase.table(TABLE_NAME).insert({
            "Email": email,
            "Role": "user"
        }).execute()
        if hasattr(new_user, "error") and new_user.error:
            raise HTTPException(status_code=500, detail=str(new_user.error))

    # Generate magic link
    try:
        payload = {
            "type": "magiclink",
            "email": email,
            "redirect_to": "http://localhost:3000"  # your frontend URL
        }
        link_info = supabase.auth.admin.generate_link(payload)

        # Access action_link properly
        action_link = getattr(link_info.properties, "action_link", None)
        if not action_link:
            raise HTTPException(status_code=500, detail="Magic link generation failed")

        return {
            "message": "Magic link generated",
            "link": action_link
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
