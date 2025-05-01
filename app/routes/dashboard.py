from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models.analysis import Analysis
from app.templates import templates
from app.auth.dependencies import login_required

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user

    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user})

@router.get("/analyses", response_class=HTMLResponse)
async def list_analyses(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user

    analyses = Analysis.get_all()
    return templates.TemplateResponse("dashboard/analyses.html", {"request": request, "analyses": analyses, "user": user})

@router.get("/create-analysis", response_class=HTMLResponse)
async def create_analysis_page(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user

    return templates.TemplateResponse("dashboard/create_analysis.html", {"request": request, "user": user})

@router.post("/create-analysis")
async def create_analysis(
    request: Request,
    name: str = Form(...),
    analytics_type: str = Form(...),
    analytics_goal: str = Form(...),
):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user

    Analysis.create({
        "name": name,
        "analytics_type": analytics_type,
        "analytics_goal": analytics_goal,
        "input_features": [],
        "preprocess_actions": [],
        "datasets": [],
        "model": "",
        "results_type_conf": [],
        "filters": []
    })
    return RedirectResponse(url="/analyses", status_code=303)

@router.get("/graph-native", response_class=HTMLResponse)
def graph_native_page(request: Request):
    return templates.TemplateResponse("dashboard/graph_native.html", {"request": request})

@router.get("/pipeline-builder", response_class=HTMLResponse)
def pipeline_builder(request: Request):
    return templates.TemplateResponse("pipeline/builder.html", {"request": request})
