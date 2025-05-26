from app.auth import create_jwt_token, verify_jwt_token
from main import app


def test_post_readers_with_vailed_token(client):
    original = app.dependency_overrides.pop(verify_jwt_token, None)

    try:
        token = create_jwt_token("test@email.com")
        _ = client.post("/readers", json={"name": "test", "email": "email@email.com"})

        response = client.get("/readers", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
    finally:
        if original:
            app.dependency_overrides[verify_jwt_token] = original


def test_post_readers_with_invalid_token(client):
    original = app.dependency_overrides.pop(verify_jwt_token, None)
    try:
        token = "invalid_token"

        _ = client.post("/readers", json={"name": "test", "email": "email@email.com"})

        response = client.get("/readers", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 401
    finally:
        if original:
            app.dependency_overrides[verify_jwt_token] = original
