from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel
from app.models import User
from . import LocalSession

router = APIRouter()


class Usermodel(BaseModel):
    email: str
    password: str


@router.post("/sign_up")
def sign_up(user: Usermodel):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        # DB connection
        db = LocalSession()
        # Check if user already exists
        check = db.query(User).filter_by(email=user.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Email already exists")
        new_user = User(email=user.email, password=bcrypt.hash(user.password))
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

        # /DB connection
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    tmp = Usermodel(email=new_user.email, password=new_user.password)
    return {"message": "User created successfully"}


@router.post("/login")
def login(user: Usermodel):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        # DB connection
        db = LocalSession()
        # Check if user exists
        check = db.query(User).filter_by(email=user.email).first()
        if not check:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        if not bcrypt.verify(user.password, check.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        # /DB connection
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Login successful"}
