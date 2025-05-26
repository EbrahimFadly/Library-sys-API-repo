from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel
from app.models import User
from . import LocalSession
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class Usermodel(BaseModel):
    email: str
    password: str


def create_jwt_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    )
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(
            token, os.getenv("JWT_SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register")
def sign_up(user: Usermodel, db: Session = Depends(LocalSession)):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
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
    return {"message": "User created successfully"}


@router.post("/login")
def login(user: Usermodel, db: Session = Depends(LocalSession)):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
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

    Session_token = create_jwt_token(user.email)
    return {"access_token": Session_token, "token_type": "bearer"}
