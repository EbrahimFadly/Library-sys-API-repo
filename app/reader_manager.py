from fastapi import APIRouter, Depends
from .auth import oauth2_scheme
from app.auth import verify_jwt_token
from .models import Reader
from . import LocalSession


router = APIRouter()


@router.get("/readers")
def get_readers(token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    db = LocalSession()
    try:
        readers = db.query(Reader).all()
        db.close()
        if not readers:
            return {"message": "No readers found"}
    except Exception as e:
        db.rollback()
        raise e
    return readers
