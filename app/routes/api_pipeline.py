from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.pipeline import Pipeline
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/save-pipeline")
async def save_pipeline(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_id = int(request.cookies.get("user_id", 0))
    name = data.get("name", "Untitled")
    graph_data = data.get("graph")

    existing = db.query(Pipeline).filter_by(user_id=user_id, name=name).first()
    if existing:
        existing.data = graph_data
    else:
        new_pipeline = Pipeline(user_id=user_id, name=name, data=graph_data)
        db.add(new_pipeline)

    db.commit()
    return JSONResponse({"status": "saved"})

@router.get("/api/load-pipeline")
def load_pipeline(request: Request, db: Session = Depends(get_db)):
    user_id = int(request.cookies.get("user_id", 0))
    pipeline = db.query(Pipeline).filter_by(user_id=user_id).first()
    if pipeline:
        return JSONResponse({"graph": pipeline.data})
    return JSONResponse({"graph": None})
