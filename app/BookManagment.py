from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import DateTime
from . import LocalSession
from .models import Book, BorrowedBook
from .auth import verify_jwt_token, oauth2_scheme


router = APIRouter()


class PostModelbook(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    copies_available: int = 1


class GetModelBorrowedBook(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    copies_available: int
    borrow_date: datetime
    return_date: datetime


class DeleteModelBook(BaseModel):
    book_id: int
    confirmation: bool


class PostModelBorrowBook(BaseModel):
    book_id: int
    reader_id: int


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
def add_book(book: PostModelbook, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        isbn=book.isbn,
        copies_available=book.copies_available,  # Default to 1 if not provided
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
def delete_book(book_toDEL: DeleteModelBook, token: str = Depends(oauth2_scheme)):
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


@router.post("/borrow")
def borrow_book(book: PostModelBorrowBook, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    db = LocalSession()
    book_to_borrow = db.query(Book).filter(Book.id == book.book_id).first()
    if not book_to_borrow:
        db.close()
        return {"message": "Book not found"}
    if book_to_borrow.copies_available <= 0:
        db.close()
        return {"message": "No copies available for borrowing"}

    book_to_borrow.copies_available -= 1
    db.add(
        BorrowedBook(
            book_id=book.book_id,
            reader_id=book.reader_id,
            borrow_date=datetime.now(),
            return_date=datetime.now() + timedelta(days=14),
        )
    )
    try:
        db.commit()
        db.refresh(book_to_borrow)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to borrow book: {e}")
        raise e
    finally:
        db.close()

    return {"message": "Book borrowed successfully", "book": book_to_borrow.title}


@router.post("/return")
def ReturnBook(book: PostModelBorrowBook, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    db = LocalSession()

    Book_to_return = (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.book_id == book.book_id,
            BorrowedBook.reader_id == book.reader_id,
        )
        .first()
    )
    if not Book_to_return:
        db.close()
        return {"message": "Borrowed book not found or already returned"}
    db.delete(Book_to_return)
    db.query(Book).filter(Book.id == book.book_id).update(
        {"copies_available": Book.copies_available + 1}
    )
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to return book: {e}")
        raise e
    finally:
        db.close()

    return {"message": "Book returned successfully"}


@router.get("/readers/{reader_id}/borrowed", response_model=List[GetModelBorrowedBook])
def get_borrowed_books(reader_id: int, token: str = Depends(oauth2_scheme)):
    verify_jwt_token(token)
    db = LocalSession()
    try:
        borrowed_books = (
            db.query(BorrowedBook)
            .join(Book)
            .filter(BorrowedBook.reader_id == reader_id)
            .all()
        )
        if not borrowed_books:
            db.close()
            return {"message": "No borrowed books found for this reader"}
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to retrieve borrowed books: {e}")
        raise e
    finally:
        books = [
            GetModelBorrowedBook(
                title=book.book.title,
                author=book.book.author,
                year=book.book.year,
                isbn=book.book.isbn,
                copies_available=book.book.copies_available,
                borrow_date=book.borrow_date,
                return_date=book.return_date,
            )
            for book in borrowed_books
        ]
        db.close()

    return books
