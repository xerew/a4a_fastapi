# --- MongoDB ---
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://admin:adminpassword@localhost:27017/fiko?authSource=admin"
# client = MongoClient(MONGO_URL)
client = AsyncIOMotorClient(MONGO_URI)
db = client["fiko"]

def get_db():
    return db

# --- PostgreSQL ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

POSTGRES_URL = "postgresql+psycopg2://postgres:root@localhost:5432/a4a_fastapi"

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()