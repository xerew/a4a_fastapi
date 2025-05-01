from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import db
from bson import ObjectId

def get_current_user(request: Request):
    user_id = request.cookies.get("user_id")
    if user_id:
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        return user
    return None

def login_required(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return user
