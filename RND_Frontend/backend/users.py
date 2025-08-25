from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from main import supabase, TABLE_NAME

router = APIRouter()

# -------------------
# Models
# -------------------
class MagicLinkRequest(BaseModel):
    Email: EmailStr

# -------------------
# Routes
# -------------------
@router.post("/request-magic-link")
def request_magic_link(data: MagicLinkRequest):
    email = data.Email

    # Ensure user exists
    existing = supabase.table(TABLE_NAME).select("*").eq("Email", email).execute()
    if not existing.data:
        supabase.table(TABLE_NAME).insert({"Email": email, "Role": "user"}).execute()

    try:
        # ✅ Use Supabase's built-in magic link email
        res = supabase.auth.sign_in_with_email(
            email=email,
            options={"redirect_to": "http://localhost:5173/magic-callback"}  # frontend route
        )

        if res.user is None:
            raise HTTPException(status_code=500, detail="Failed to send magic link email")

        return {"message": "Magic link sent! Check your email."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------
# Callback Route
# -------------------
@router.get("/callback")
def magic_link_callback(request: Request):
    """
    Handles the magic link callback from Supabase.
    Supabase redirects here after user clicks the magic link.
    """
    # Supabase appends access_token and refresh_token in the URL fragment.
    # Fragments are not sent to server; frontend reads them.
    frontend_url = "http://localhost:5173/magic-callback"  # React route
    return RedirectResponse(url=frontend_url + str(request.url.query))
