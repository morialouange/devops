import pytest
import json
from app import create_app, db


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def register_user(client, username="testuser", email="test@example.com", password="secret123"):
    return client.post(
        "/api/auth/register",
        data=json.dumps({"username": username, "email": email, "password": password}),
        content_type="application/json",
    )


def login_user(client, login="testuser", password="secret123"):
    return client.post(
        "/api/auth/login",
        data=json.dumps({"login": login, "password": password}),
        content_type="application/json",
    )


def get_token(client):
    register_user(client)
    resp = login_user(client)
    return resp.get_json()["access_token"]


class TestRegister:
    def test_register_success(self, client):
        resp = register_user(client)
        assert resp.status_code == 201
        assert "user" in resp.get_json()

    def test_register_missing_fields(self, client):
        resp = client.post(
            "/api/auth/register",
            data=json.dumps({"username": "test"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_register_short_password(self, client):
        resp = register_user(client, password="123")
        assert resp.status_code == 400

    def test_register_duplicate_username(self, client):
        register_user(client)
        resp = register_user(client, email="other@example.com")
        assert resp.status_code == 409

    def test_register_duplicate_email(self, client):
        register_user(client)
        resp = register_user(client, username="other")
        assert resp.status_code == 409


class TestLogin:
    def test_login_success(self, client):
        register_user(client)
        resp = login_user(client)
        assert resp.status_code == 200
        assert "access_token" in resp.get_json()

    def test_login_wrong_password(self, client):
        register_user(client)
        resp = login_user(client, password="wrongpass")
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = login_user(client, login="nobody")
        assert resp.status_code == 401

    def test_login_with_email(self, client):
        register_user(client)
        resp = login_user(client, login="test@example.com")
        assert resp.status_code == 200


class TestProtectedRoutes:
    def test_get_profile(self, client):
        token = get_token(client)
        resp = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["user"]["username"] == "testuser"

    def test_get_profile_no_token(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_update_profile(self, client):
        token = get_token(client)
        resp = client.put(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            data=json.dumps({"username": "newname"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["user"]["username"] == "newname"

    def test_change_password(self, client):
        token = get_token(client)
        resp = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            data=json.dumps({"current_password": "secret123", "new_password": "newsecret456"}),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_change_password_wrong_current(self, client):
        token = get_token(client)
        resp = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            data=json.dumps({"current_password": "wrong", "new_password": "newsecret456"}),
            content_type="application/json",
        )
        assert resp.status_code == 401
