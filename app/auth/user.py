from app.core.config import SessionLocal
from app.models.user_sql import UserSQL
from passlib.hash import bcrypt

def get_user_by_username(username: str):
    db = SessionLocal()
    user = db.query(UserSQL).filter(UserSQL.username == username).first()
    db.close()
    return user

def get_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(UserSQL).filter(UserSQL.email == email).first()
    db.close()
    return user

def create_user(username, first_name, last_name, email, password):
    db = SessionLocal()
    hashed_password = bcrypt.hash(password)

    new_user = UserSQL(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)
