from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from main import supabase, TABLE_NAME
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re

router = APIRouter()

class MagicLinkRequest(BaseModel):
    Email: EmailStr

@router.post("/request-magic-link")
def request_magic_link(data: MagicLinkRequest):
    email = data.Email

    # Check if user exists in Users table
    user_check = supabase.table(TABLE_NAME).select("Role").eq("Email", email).execute()
    if not user_check.data:
        raise HTTPException(status_code=404, detail="User not found")

    # Get role from table
    role = user_check.data[0]["Role"].strip().lower()
    print("DEBUG ROLE CHECK:", role, "for email:", email)  # 👈 add this
    # Decide redirect based on role
    if role == "admin":
        redirect_url = "http://localhost:5173/admin"
    else:
        redirect_url = "http://localhost:5173/dashboard"

    try:
        # Generate magic link using Supabase Admin API
        payload = {
            "type": "magiclink",
            "email": email,
            "redirect_to": redirect_url
        }
        link_info = supabase.auth.admin.generate_link(payload)

        action_link = getattr(link_info.properties, "action_link", None)
        if not action_link:
            raise HTTPException(status_code=500, detail="Magic link generation failed")

        # Force override redirect_to in action link
        if "redirect_to=" in action_link:
            action_link = re.sub(
                r"redirect_to=[^&]+",
                f"redirect_to={redirect_url}",
                action_link
            )
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
        body = f"Hello,\n\nClick this link to login: {action_link}\n\nThis link expires in a few minutes."
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
