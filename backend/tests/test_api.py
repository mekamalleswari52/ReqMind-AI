import io

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.project import Project


client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Project).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def test_register_and_login_flow():
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"

    login = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    assert token

    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200, me.text
    assert me.json()["email"] == "test@example.com"


def test_project_creation_requires_auth_and_returns_owner_project():
    register = client.post(
        "/api/auth/register",
        json={
            "full_name": "Owner",
            "email": "owner@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    token = client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "secret123"},
    ).json()["access_token"]

    response = client.post(
        "/api/projects/",
        json={"name": "Alpha Project", "description": "Demo"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Alpha Project"
    assert body["owner_id"] == 1

    no_auth = client.post(
        "/api/projects/",
        json={"name": "Nope"},
    )
    assert no_auth.status_code == 401


def test_document_upload_works_with_file_and_auth():
    register = client.post(
        "/api/auth/register",
        json={
            "full_name": "Doc Owner",
            "email": "doc@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    token = client.post(
        "/api/auth/login",
        json={"email": "doc@example.com", "password": "secret123"},
    ).json()["access_token"]

    project = client.post(
        "/api/projects/",
        json={"name": "Docs", "description": "Document project"},
        headers={"Authorization": f"Bearer {token}"},
    )
    project_id = project.json()["id"]

    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.txt", b"REQ-1 The system shall allow login.", "text/plain")},
        data={"project_id": str(project_id)},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["filename"] == "sample.txt"
    assert "REQ-1" in payload["content"]
