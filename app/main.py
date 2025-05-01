from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.auth.routes import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.templates import templates
from fastapi.responses import RedirectResponse
from app.auth.dependencies import get_current_user
from app.auth.dependencies import login_required

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth_router)
app.include_router(dashboard_router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user

    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user})

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/login")