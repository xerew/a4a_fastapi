from app.core.config import db
from passlib.hash import bcrypt

class User:
    collection = db["users"]

    @staticmethod
    def find_by_username(username):
        return User.collection.find_one({"username": username})

    @staticmethod
    def create_user(username, first_name, last_name, email, password):
        hashed_password = bcrypt.hash(password)
        return User.collection.insert_one({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
        })

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.verify(password, hashed)
