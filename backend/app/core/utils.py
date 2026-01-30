"""
Utility functions
"""
import re
from typing import Optional
import math


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email address

    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    return True, None


def calculate_shadow_coefficient(solar_altitude: float, building_height: float) -> float:
    """
    Calculate shadow length coefficient based on solar altitude angle

    Args:
        solar_altitude: Solar altitude angle in degrees
        building_height: Building height in meters

    Returns:
        Shadow length coefficient (shadow_length / building_height)
    """
    if solar_altitude <= 0:
        return float('inf')

    # Convert altitude to radians
    altitude_rad = math.radians(solar_altitude)

    # Calculate shadow length coefficient
    # shadow_length = building_height / tan(altitude_angle)
    # coefficient = shadow_length / building_height = 1 / tan(altitude_angle)
    coefficient = 1.0 / math.tan(altitude_rad)

    return coefficient


def geojson_to_wkt(geojson: dict) -> str:
    """
    Convert GeoJSON Polygon to WKT (Well-Known Text) format

    Args:
        geojson: GeoJSON Polygon object

    Returns:
        WKT string
    """
    if geojson.get("type") != "Polygon":
        raise ValueError("Only Polygon type is supported")

    coordinates = geojson.get("coordinates", [])
    if not coordinates:
        raise ValueError("No coordinates found")

    # Convert coordinates to WKT format
    rings = []
    for ring in coordinates:
        coord_strs = [f"{lng} {lat}" for lng, lat in ring]
        rings.append(f"({', '.join(coord_strs)})")

    wkt = f"POLYGON({', '.join(rings)})"
    return wkt


def wkt_to_geojson(wkt: str) -> dict:
    """
    Convert WKT (Well-Known Text) to GeoJSON Polygon format

    Args:
        wkt: WKT string

    Returns:
        GeoJSON Polygon object
    """
    # Simple parser for POLYGON WKT
    # Note: For production, use a proper library like geojson

    import re

    # Extract coordinates
    match = re.search(r'POLYGON\s*\((.+)\)', wkt, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid WKT format")

    coords_str = match.group(1)

    # Parse rings
    rings = []
    # This is a simplified parser - use shapely or similar in production
    coord_matches = re.findall(r'\(([^)]+)\)', coords_str)
    for coord_match in coord_matches:
        coords = []
        coord_pairs = coord_match.split(',')
        for pair in coord_pairs:
            parts = pair.strip().split()
            if len(parts) >= 2:
                lng, lat = float(parts[0]), float(parts[1])
                coords.append([lng, lat])
        rings.append(coords)

    return {
        "type": "Polygon",
        "coordinates": rings
    }
