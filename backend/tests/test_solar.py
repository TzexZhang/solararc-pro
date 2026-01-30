"""
Solar Position Calculation Tests
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Create a test client
    """
    return TestClient(app)


def test_calculate_solar_position(client):
    """
    Test solar position calculation
    """
    response = client.get(
        "/api/v1/solar/position",
        params={
            "lat": 39.9042,
            "lng": 116.4074,
            "date": "2024-06-21",
            "hour": 12,
            "minute": 0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "solar_altitude" in data["data"]
    assert "solar_azimuth" in data["data"]
    assert "sunrise_time" in data["data"]
    assert "sunset_time" in data["data"]


def test_calculate_daily_positions(client):
    """
    Test daily solar positions calculation
    """
    response = client.get(
        "/api/v1/solar/daily-positions",
        params={
            "lat": 39.9042,
            "lng": 116.4074,
            "date": "2024-06-21"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "positions" in data["data"]
    assert len(data["data"]["positions"]) == 24
