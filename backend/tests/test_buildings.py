"""
Building Data Tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape

from app.main import app
from app.database import Base, get_db
from app.models.building import Building
from shapely.geometry import Polygon

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


def test_get_buildings_in_bbox(client, db_session):
    """
    Test getting buildings within bounding box
    """
    # Create a test building
    footprint = Polygon([(0, 0), (0, 0.001), (0.001, 0.001), (0.001, 0), (0, 0)])
    building = Building(
        name="Test Building",
        building_type="residential",
        footprint=from_shape(footprint, srid=4326),
        total_height=100.0,
        floor_area=5000.0,
        floor_count=30,
        city="Beijing"
    )
    db_session.add(building)
    db_session.commit()

    # Query buildings
    response = client.get(
        "/api/v1/buildings/bbox",
        params={
            "min_lat": -0.001,
            "max_lat": 0.002,
            "min_lng": -0.001,
            "max_lng": 0.002
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["data"]["buildings"]) >= 1


def test_get_building_by_id(client, db_session):
    """
    Test getting a single building by ID
    """
    # Create a test building
    footprint = Polygon([(0, 0), (0, 0.001), (0.001, 0.001), (0.001, 0), (0, 0)])
    building = Building(
        name="Test Building",
        building_type="commercial",
        footprint=from_shape(footprint, srid=4326),
        total_height=150.0,
        city="Shanghai"
    )
    db_session.add(building)
    db_session.commit()

    # Get building by ID
    response = client.get(f"/api/v1/buildings/{building.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert data["data"]["id"] == building.id
    assert data["data"]["name"] == "Test Building"
