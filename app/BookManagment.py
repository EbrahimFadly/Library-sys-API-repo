from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import LocalSession
from .models import Book
from .auth import verify_jwt_token, oauth2_scheme


router = APIRouter()


class bookModel(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    copies_available: int = 1


class BookDeletionModel(BaseModel):
    book_id: int
    confirmation: bool


@router.get("/books")
def get_books(token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    db = LocalSession()
    books = db.query(Book).all()
    db.close()
    if not books:
        return {"message": "No books found"}
    return books


@router.post("/books")
def add_book(book: bookModel, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        isbn=book.isbn,
        copies_available=book.copies_available,
    )
    db = LocalSession()
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to add book: {e}")
        raise e
    finally:
        db.close()
    return {"message": "Book added successfully", "book": book.title}


@router.delete("/books")
def delete_book(book_toDEL: BookDeletionModel, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    if not book_toDEL.confirmation:
        return {"message": "Deletion not confirmed"}
    db = LocalSession()
    book = db.query(Book).filter(Book.id == book_toDEL.book_id).first()
    if not book:
        db.close()
        return {"message": "Book not found"}
    try:
        db.delete(book)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to delete book: {e}")
        raise e
    finally:
        db.close()
    return {"message": "Book deleted successfully", "book": book.title}
