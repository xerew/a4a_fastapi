from app.core.config import db
from bson.objectid import ObjectId
from datetime import datetime

class Analysis:
    collection = db["analysis"]

    @staticmethod
    def get_all():
        return list(Analysis.collection.find())

    @staticmethod
    def get_by_id(analysis_id):
        return Analysis.collection.find_one({"_id": ObjectId(analysis_id)})

    @staticmethod
    def create(data):
        data["date_created"] = datetime.utcnow()
        data["date_updated"] = datetime.utcnow()
        return Analysis.collection.insert_one(data).inserted_id

    @staticmethod
    def update(analysis_id, updates):
        updates["date_updated"] = datetime.utcnow()
        return Analysis.collection.update_one({"_id": ObjectId(analysis_id)}, {"$set": updates})

    @staticmethod
    def delete(analysis_id):
        return Analysis.collection.delete_one({"_id": ObjectId(analysis_id)})
