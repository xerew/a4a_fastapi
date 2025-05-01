from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
MONGO_DB = "a4a"

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]