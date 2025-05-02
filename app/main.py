from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth.routes import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.templates import templates
from app.auth.dependencies import get_current_user, login_required
from app.core.config import Base, engine
from app.dash.graph import dash_app
from starlette.middleware.wsgi import WSGIMiddleware
from app.routes import api_pipeline
from app.models.pipeline import Pipeline

app = FastAPI()

# Create tables at startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(api_pipeline.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user})

app.mount("/graph", WSGIMiddleware(dash_app.server))

try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
except Exception as e:
    print("❌ Error creating tables:", e)