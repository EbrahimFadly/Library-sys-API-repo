def test_get_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {"message": "No books found"}


def test_add_book(client):
    response = client.post(
        "/books",
        json={
            "title": "test book",
            "author": "author",
            "year": 1949,
            "isbn": "978451524935",
            "copies_available": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"


def test_borrow_book(client):
    client.post("/readers", json={"name": "Alice", "email": "test@email.com"})

    client.post(
        "/books",
        json={
            "title": "test book",
            "author": "author",
            "year": 1949,
            "isbn": "978451524935",
            "copies_available": 2,
        },
    )

    response = client.post("/borrow", json={"book_id": 1, "reader_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Book borrowed successfully"


def test_return_book(client):
    # adding a book to return
    client.post(
        "/books",
        json={
            "title": "test book",
            "author": "author",
            "year": 1949,
            "isbn": "978451524935",
            "copies_available": 1,
        },
    )

    response = client.post("/borrow", json={"book_id": 1, "reader_id": 1})
    response = client.post("/return", json={"book_id": 1, "reader_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Book returned successfully"


def test_delete_book(client):
    # adding a book to delete
    client.post(
        "/books",
        json={
            "title": "test book",
            "author": "author",
            "year": 1949,
            "isbn": "978451524935",
            "copies_available": 1,
        },
    )
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
