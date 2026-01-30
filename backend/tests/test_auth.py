"""
Authentication Tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """
    Create a test database session
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """
    Create a test client with database override
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_register_user(client):
    """
    Test user registration
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "nickname": "Test User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["code"] == 201
    assert "user_id" in data["data"]


def test_login_user(client, db_session):
    """
    Test user login
    """
    # Create a test user first
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        nickname="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    # Test login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_get_current_user(client, db_session):
    """
    Test getting current user info
    """
    # Create and login user
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        nickname="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    # Login to get token
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    token = login_response.json()["data"]["access_token"]

    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert data["data"]["email"] == "test@example.com"
