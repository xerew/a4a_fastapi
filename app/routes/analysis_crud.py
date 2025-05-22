from fastapi import APIRouter, Depends, HTTPException
from app.core.db import get_db
from app.models.analysis import AnalysisCreate, AnalysisInDB
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/", response_model=AnalysisInDB)
async def create_analysis(data: AnalysisCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    now = datetime.utcnow()
    doc = data.dict()
    doc["date_created"] = now
    doc["date_updated"] = now
    result = await db.analysis.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return AnalysisInDB(**doc)

@router.get("/", response_model=List[AnalysisInDB])
async def list_analyses(db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db.analysis.find()
    return [AnalysisInDB(**{**doc, "_id": str(doc["_id"])}) async for doc in cursor]

@router.get("/{analysis_id}", response_model=AnalysisInDB)
async def get_analysis(analysis_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = await db.analysis.find_one({"_id": ObjectId(analysis_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisInDB(**{**doc, "_id": str(doc["_id"])})

@router.put("/{analysis_id}")
async def update_analysis(analysis_id: str, data: AnalysisCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.analysis.update_one(
        {"_id": ObjectId(analysis_id)},
        {"$set": {**data.dict(), "date_updated": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Update failed")
    return {"success": True}

@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.analysis.delete_one({"_id": ObjectId(analysis_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Delete failed")
    return {"success": True}
