def test_get_readers_empty(client):
    response = client.get("/readers")
    assert response.status_code == 200
    assert response.json() == {"message": "No readers found"}


def test_add_reader(client):
    response = client.post(
        "/readers", json={"name": "John Doe", "email": "test@email.com"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Reader added successfully",
        "reader": "John Doe",
    }
