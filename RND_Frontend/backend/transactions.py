# backend/transactions.py
from fastapi import APIRouter, Depends, HTTPException
from main import supabase  # ✅ use the shared Supabase client
from auth import get_current_user  # validating JWT tokens

router = APIRouter()

@router.get("/")
def get_transactions(user: dict = Depends(get_current_user)):
    """
    Returns transactions filtered by user ID & role.
    """
    user_id = user["id"]
    role = user["role"]

    if role == "admin":
        # Admin sees all transactions
        response = supabase.table("Transactions").select("*").execute()
    else:
        # Investor sees only their own transactions
        response = (
            supabase.table("Transactions")
            .select("*")
            .eq("investorId", user_id)
            .execute()
        )

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)

    return response.data
