from fastapi import Request
from starlette.responses import RedirectResponse
from app.core.config import SessionLocal
from app.models.user_sql import UserSQL

def get_current_user(request: Request):
    user_id = request.cookies.get("user_id")
    if user_id is None:
        return None

    db = SessionLocal()
    user = db.query(UserSQL).filter(UserSQL.id == int(user_id)).first()
    db.close()
    return user

def login_required(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return user
