import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.databases.relational import Base
from app.main import app as fastapi_app, get_settings
from app.settings import get_sqldb_settings, get_mongodb_settings


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_document_db():
    return None


def override_get_secret_dir():
    return "../resources"


def override_get_settings():
    return None
def override_get_sqldb_settings():
    return None
def override_get_mongodb_settings():
    return None

fastapi_app.dependency_overrides[get_settings] = override_get_settings
fastapi_app.dependency_overrides[get_sqldb_settings] = override_get_sqldb_settings
astapi_app.dependency_overrides[get_mongodb_settings] = override_get_mongodb_settings


# app.settings.get_secret_dir = override_get_secret_dir
# app.settings.SQLDBSettings.Config.secrets_dir = override_get_secret_dir()
fastapi_app.dependency_overrides[app.databases.relational.get_relationaldb] = override_get_db
fastapi_app.dependency_overrides[app.databases.document.get_document_db] = override_get_document_db
# fastapi_app.dependency_overrides[get_secret_dir] = override_get_secret_dir


@pytest.fixture(scope="session", autouse=True)
def test_config(monkeypatch):
    print(os.environ.get("SECRETS_DIR"))
    monkeypatch.setenv("SECRETS_DIR", "./resources")


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_create_user(client):
    # response = client.post(
    #     "/users/",
    #     json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    # )
    response = client.post(
            fastapi_app.url_path_for("create_user",
                             {
                                 "username":   "jsmith",
                                 "email":      "johnsmith@test.com",
                                 "first_name": "John",
                                 "last_name":  "Smith",
                                 "password":   "pass4test!",
                                 "role":       "test"
                             }))
    assert response.status_code == 201\
    #     , response.text
    # data = response.json()
    # assert data["email"] == "deadpool@example.com"
    # assert "id" in data
    # user_id = data["id"]
    #
    # response = client.get(f"/users/{user_id}")
    # assert response.status_code == 200, response.text
    # data = response.json()
    # assert data["email"] == "deadpool@example.com"
    # assert data["id"] == user_id
