from fastapi import APIRouter, HTTPException, Depends, Request, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from main import supabase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from jose import JWTError, jwt

router = APIRouter()

# -------------------------------
# JWT Authentication Setup
# -------------------------------
security = HTTPBearer()
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        name: str = payload.get("user_metadata", {}).get("name") or email  # Use name from JWT

        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"id": user_id, "email": email, "role": role, "Name": name}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------------
# Current User Endpoint (JWT-based)
# -------------------------------
@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    """
    Returns current logged-in user info from JWT token.
    """
    return JSONResponse(content=user)

# -------------------------------
# Cookie-Based Auth (safer than localStorage)
# -------------------------------
def get_current_user_from_cookie(session: str = Cookie(None)):
    if not session:
        raise HTTPException(status_code=401, detail="No session cookie found")

    try:
        payload = jwt.decode(session, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        name: str = payload.get("user_metadata", {}).get("name") or email

        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid session cookie")

        return {"id": user_id, "email": email, "role": role, "Name": name}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired session cookie")

@router.post("/auth/callback")
def auth_callback(token: str, response: Response):
    """
    Accepts Supabase token and stores it in a secure HttpOnly cookie.
    """
    if not token:
        raise HTTPException(status_code=400, detail="Missing token")

    try:
        # Validate the JWT (optional but good practice)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid Supabase token")

        # ✅ Set HttpOnly cookie
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24  # 1 day expiry
        )
        return {"message": "Session cookie set"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/me-cookie")
def get_me_cookie(user: dict = Depends(get_current_user_from_cookie)):
    """
    Returns user info from cookie-based session.
    """
    return JSONResponse(content=user)

# -------------------------------
# Magic Link Endpoint
# -------------------------------
class MagicLinkRequest(BaseModel):
    Email: EmailStr

@router.post("/request-magic-link")
def request_magic_link(data: MagicLinkRequest):
    email = data.Email

    # Pull role and Name from Supabase Users table
    user_check = supabase.table("Users").select("Role, Name").eq("Email", email).execute()
    if not user_check.data:
        raise HTTPException(status_code=404, detail="User not found")

    role = user_check.data[0]["Role"].strip().lower()
    name = user_check.data[0]["Name"]
    redirect_url = "http://localhost:5173/admin" if role == "admin" else "http://localhost:5173/dashboard"

    try:
        # Include Name in JWT payload via Supabase admin.generate_link
        payload = {
            "type": "magiclink",
            "email": email,
            "redirect_to": redirect_url,
            "user_metadata": {"name": name}
        }
        link_info = supabase.auth.admin.generate_link(payload)
        action_link = getattr(link_info.properties, "action_link", None)
        if not action_link:
            raise HTTPException(status_code=500, detail="Magic link generation failed")

        # Ensure redirect_to is correct
        if "redirect_to=" in action_link:
            action_link = re.sub(r"redirect_to=[^&]+", f"redirect_to={redirect_url}", action_link)
        else:
            action_link += f"&redirect_to={redirect_url}"

        # -------------------------------
        # Send email via SMTP
        # -------------------------------
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        if not smtp_user or not smtp_pass:
            raise HTTPException(status_code=500, detail="SMTP credentials not set in .env")

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = "Your Magic Login Link"
        body = f"Hello {name},\n\nClick this link to login: {action_link}\n\nThis link expires in a few minutes."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        print("Magic link sent via email:", email)
        return {"message": f"Magic link sent! Check {email} for the email."}

    except Exception as e:
        print("Exception in request_magic_link:", e)
        raise HTTPException(status_code=500, detail=str(e))
