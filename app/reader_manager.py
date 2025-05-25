from fastapi import APIRouter, Depends
from app.auth import verify_jwt_token
from .models import Reader
from . import LocalSession
from pydantic import BaseModel
from sqlalchemy.orm import Session


router = APIRouter()


class ReaderModel(BaseModel):
    name: str
    email: str


@router.get("/readers")
def get_readers(
    email: str = Depends(verify_jwt_token), db: Session = Depends(LocalSession)
):
    try:
        readers = db.query(Reader).all()
        db.close()
        if not readers:
            return {"message": "No readers found"}
    except Exception as e:
        db.rollback()
        raise e
    return readers


@router.post("/readers")
def add_reader(
    reader: ReaderModel,
    email: str = Depends(verify_jwt_token),
    db: Session = Depends(LocalSession),
):
    new_reader = Reader(name=reader.name, email=reader.email)
    try:
        db.add(new_reader)
        db.commit()
        db.refresh(new_reader)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to add reader: {e}")
        raise e
    finally:
        db.close()
    return {"message": "Reader added successfully", "reader": reader.name}
