from fastapi import APIRouter
from . import LocalSession
from .models import Book

router = APIRouter()


@router.get("/books")
def get_books():
    db = LocalSession()
    books = db.query(Book).all()
    return books
