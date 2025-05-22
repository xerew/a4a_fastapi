from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models.analysis import Analysis
from app.templates import templates
from app.auth.dependencies import login_required
from app.core.config import get_db
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import json
from app.schemas.collection_schemas import collection_field_definitions


templates = Jinja2Templates(directory="app/templates")
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

@router.get("/list_collections", response_class=HTMLResponse)
async def list_collections(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    collections = await db.list_collection_names()
    return templates.TemplateResponse("dashboard/list_collections.html", {"request": request, "collections": collections})

@router.get("/collection/{name}", response_class=HTMLResponse)
async def view_collection(name: str, request: Request, db=Depends(get_db)):
    cursor = db[name].find()
    docs = [ {**doc, "_id": str(doc["_id"])} async for doc in cursor ]
    return templates.TemplateResponse("dashboard/collection_view.html", {"request": request, "collection_name": name, "documents": docs})

@router.get("/collection/{name}/edit/{doc_id}", response_class=HTMLResponse)
async def edit_doc_form(name: str, doc_id: str, request: Request, db=Depends(get_db)):
    collection = db[name]
    doc = await collection.find_one({"_id": ObjectId(doc_id)})

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc["_id"] = str(doc["_id"])
    return templates.TemplateResponse("dashboard/edit_doc.html", {
        "request": request,
        "collection_name": name,
        "doc": doc
    })

@router.post("/collection/{name}/edit/{doc_id}")
async def edit_doc_submit(name: str, doc_id: str, request: Request, db=Depends(get_db)):
    form = await request.form()
    updates = {key: form[key] for key in form if key != "_id"}

    # Convert to appropriate types if needed (for now: plain strings)
    await db[name].update_one({"_id": ObjectId(doc_id)}, {"$set": updates})
    return RedirectResponse(url=f"/collection/{name}", status_code=303)

@router.get("/collection/{name}/create", response_class=HTMLResponse)
async def create_doc_form(name: str, request: Request):
    fields = collection_field_definitions.get(name)
    if not fields:
        raise HTTPException(status_code=404, detail=f"No form defined for collection '{name}'")
    return templates.TemplateResponse("dashboard/create_doc.html", {
        "request": request,
        "collection_name": name,
        "fields": fields
    })

@router.post("/collection/{name}/create")
async def create_doc_submit(name: str, request: Request, db=Depends(get_db)):
    form = await request.form()
    form = dict(form)

    schema = collection_field_definitions.get(name)
    if not schema:
        raise HTTPException(status_code=400, detail="Invalid collection schema")

    doc = {}
    for field in schema:
        key = field["name"]
        val = form.get(key, "")

        if field["type"] == "list":
            doc[key] = [v.strip() for v in val.split(",") if v.strip()]
        elif field["type"] == "json":
            try:
                doc[key] = json.loads(val)
            except:
                doc[key] = []
        else:
            doc[key] = val

    from datetime import datetime
    doc["date_created"] = datetime.utcnow().isoformat()
    doc["date_updated"] = datetime.utcnow().isoformat()

    await db[name].insert_one(doc)
    return RedirectResponse(url=f"/collection/{name}", status_code=303)

@router.post("/collection/{name}/delete/{doc_id}")
async def delete_doc(name: str, doc_id: str, db=Depends(get_db)):
    await db[name].delete_one({"_id": ObjectId(doc_id)})
    return RedirectResponse(url=f"/collection/{name}", status_code=303)
