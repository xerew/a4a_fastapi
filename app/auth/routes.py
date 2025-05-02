from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from app.auth.user import get_user_by_username, get_user_by_email, create_user,verify_password
from app.templates import templates

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("account/login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_by_username(username)
    if user and verify_password(password, user.password):
        response = RedirectResponse(url="/dashboard", status_code=303)

        # ✅ Set persistent, secure cookie for 30 days
        response.set_cookie(
            key="user_id",
            value=str(user.id),
            max_age=30 * 24 * 60 * 60,  # 30 days in seconds
            httponly=True,
            samesite="lax",
            secure=False  # Set to True in production with HTTPS
        )

        return response

    return templates.TemplateResponse("account/login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("account/register.html", {"request": request})

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        return templates.TemplateResponse("account/register.html", {
            "request": request,
            "error": "Passwords do not match"
        })

    if get_user_by_username(username):
        return templates.TemplateResponse("account/register.html", {
            "request": request,
            "error": "Username already taken"
        })

    if get_user_by_email(email):
        return templates.TemplateResponse("account/register.html", {
            "request": request,
            "error": "Email already in use"
        })

    create_user(username, first_name, last_name, email, password)

    return RedirectResponse(url="/login", status_code=303)

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("user_id")
    return response
