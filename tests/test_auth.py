def test_register_user(client):
    response = client.post(
        "/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_register_existing_user(client):
    _ = client.post(
        "/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    response = client.post(
        "/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_login_user(client):
    _ = client.post(
        "/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    response = client.post(
        "/login",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    _ = client.post(
        "/register", json={"email": "testuser@example.com", "password": "password"}
    )
    response = client.post(
        "/login", json={"email": "testuser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"
