import os
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- MongoDB ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:adminpassword@localhost:27017/fiko?authSource=admin")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["fiko"]

def get_db():
    return db

# --- PostgreSQL ---
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://postgres:root@localhost:5432/a4a_fastapi")
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
