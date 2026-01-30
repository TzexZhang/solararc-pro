"""
Shadow Calculation Service
"""
from datetime import datetime, date
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

try:
    from shapely.geometry import Polygon, Point, MultiPolygon
    from shapely.ops import unary_union
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False
    print("Warning: shapely not available. Shadow calculations will be limited.")

from app.services.solar_service import calculate_solar_position
from app.core.utils import calculate_shadow_coefficient


def calculate_building_shadow(
    building_footprint: Dict[str, Any],
    building_height: float,
    lat: float,
    lng: float,
    analysis_date: Optional[str] = None,
    hour: int = 12,
    minute: int = 0
) -> Tuple[Dict[str, Any], float]:
    """
    Calculate shadow polygon for a building

    Args:
        building_footprint: GeoJSON Polygon of building footprint
        building_height: Building height in meters
        lat: Latitude
        lng: Longitude
        analysis_date: Analysis date (YYYY-MM-DD)
        hour: Hour (0-23)
        minute: Minute (0-59)

    Returns:
        Tuple of (shadow_polygon_geojson, shadow_area_sqm)
    """
    if not SHAPELY_AVAILABLE:
        raise Exception("Shapely library is required for shadow calculations")

    # Get solar position
    solar_pos = calculate_solar_position(lat, lng, analysis_date, hour, minute)
    solar_altitude = solar_pos["solar_altitude"]
    solar_azimuth = solar_pos["solar_azimuth"]

    # If sun is below horizon, no shadow
    if solar_altitude <= 0:
        return None, 0.0

    # Parse building footprint
    if building_footprint.get("type") != "Polygon":
        raise ValueError("Building footprint must be a Polygon")

    coordinates = building_footprint.get("coordinates", [])
    if not coordinates:
        raise ValueError("No coordinates in building footprint")

    # Get exterior ring
    exterior_coords = coordinates[0]

    # Convert to Shapely polygon
    building_poly = Polygon(exterior_coords)

    # Calculate shadow
    shadow_poly = _project_shadow(building_poly, building_height, solar_altitude, solar_azimuth)

    if shadow_poly is None or shadow_poly.is_empty:
        return None, 0.0

    # Convert to GeoJSON
    shadow_geojson = _shapely_to_geojson(shadow_poly)

    # Calculate area (approximate, in square degrees)
    # For accurate area in square meters, need to use projection
    area = shadow_poly.area

    # Rough conversion to square meters (at the given latitude)
    # This is an approximation
    meters_per_degree = 111320 * np.cos(np.radians(lat))
    area_sqm = area * (meters_per_degree ** 2)

    return shadow_geojson, round(area_sqm, 2)


def calculate_shadow_overlap(
    target_building_footprint: Dict[str, Any],
    surrounding_shadows: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate shadow overlap on target building

    Args:
        target_building_footprint: GeoJSON Polygon of target building
        surrounding_shadows: List of shadow polygons (GeoJSON)

    Returns:
        Dictionary containing overlap analysis
    """
    if not SHAPELY_AVAILABLE:
        raise Exception("Shapely library is required for shadow overlap calculations")

    # Parse target building
    target_coords = target_building_footprint.get("coordinates", [])
    target_poly = Polygon(target_coords[0])

    # Calculate self-shadow area
    # (This would be the building's own shadow on itself - simplified as 0 for now)
    self_shadow_area = 0.0

    # Union all surrounding shadows
    shadow_polys = []
    for shadow in surrounding_shadows:
        if shadow.get("type") == "Polygon":
            coords = shadow.get("coordinates", [])
            if coords:
                shadow_polys.append(Polygon(coords[0]))

    if not shadow_polys:
        return {
            "self_shadow_area": 0.0,
            "projected_shadow_area": 0.0,
            "overlap_area": 0.0,
            "overlap_details": []
        }

    # Merge all shadows
    merged_shadows = unary_union(shadow_polys)

    # Calculate projected shadow area on target building
    intersection = target_poly.intersection(merged_shadows)
    projected_shadow_area = intersection.area

    # Calculate overlap area (in square meters, approximation)
    meters_per_degree = 111320  # rough approximation
    overlap_area_sqm = projected_shadow_area * (meters_per_degree ** 2)

    # Calculate individual overlaps
    overlap_details = []
    for i, shadow_poly in enumerate(shadow_polys):
        overlap = target_poly.intersection(shadow_poly)
        if not overlap.is_empty:
            overlap_area_sqm = overlap.area * (meters_per_degree ** 2)
            overlap_details.append({
                "building_id": f"building_{i}",
                "overlap_area": round(overlap_area_sqm, 2)
            })

    return {
        "self_shadow_area": round(self_shadow_area, 2),
        "projected_shadow_area": round(projected_shadow_area, 2),
        "overlap_area": round(overlap_area_sqm, 2),
        "overlap_details": overlap_details
    }


def calculate_shadow_comparison(
    building_footprint: Dict[str, Any],
    building_height: float,
    lat: float,
    lng: float,
    hour: int = 12
) -> Dict[str, Any]:
    """
    Compare shadows on winter solstice vs summer solstice

    Args:
        building_footprint: GeoJSON Polygon of building footprint
        building_height: Building height in meters
        lat: Latitude
        lng: Longitude
        hour: Hour to compare (default: 12, solar noon)

    Returns:
        Dictionary containing shadow comparison
    """
    # Winter solstice (approximately December 22)
    winter_shadow, winter_area = calculate_building_shadow(
        building_footprint,
        building_height,
        lat,
        lng,
        "2024-12-22",
        hour,
        0
    )

    # Summer solstice (approximately June 21)
    summer_shadow, summer_area = calculate_building_shadow(
        building_footprint,
        building_height,
        lat,
        lng,
        "2024-06-21",
        hour,
        0
    )

    # Calculate shadow length coefficients
    solar_pos_winter = calculate_solar_position(lat, lng, "2024-12-22", hour, 0)
    solar_pos_summer = calculate_solar_position(lat, lng, "2024-06-21", hour, 0)

    winter_coefficient = calculate_shadow_coefficient(
        solar_pos_winter["solar_altitude"],
        building_height
    )
    summer_coefficient = calculate_shadow_coefficient(
        solar_pos_summer["solar_altitude"],
        building_height
    )

    # Calculate ratio
    ratio = winter_coefficient / summer_coefficient if summer_coefficient > 0 else 0

    return {
        "winter_solstice": {
            "date": "2024-12-22",
            "shadow_polygon": winter_shadow,
            "shadow_area": winter_area,
            "shadow_length_coefficient": round(winter_coefficient, 2)
        },
        "summer_solstice": {
            "date": "2024-06-21",
            "shadow_polygon": summer_shadow,
            "shadow_area": summer_area,
            "shadow_length_coefficient": round(summer_coefficient, 2)
        },
        "ratio": round(ratio, 2)
    }


def _project_shadow(
    building_poly: Polygon,
    height: float,
    solar_altitude: float,
    solar_azimuth: float
) -> Polygon:
    """
    Project building shadow based on solar position

    Args:
        building_poly: Building footprint polygon
        height: Building height
        solar_altitude: Solar altitude angle in degrees
        solar_azimuth: Solar azimuth angle in degrees

    Returns:
        Shadow polygon
    """
    # Convert angles to radians
    alt_rad = np.radians(solar_altitude)
    az_rad = np.radians(solar_azimuth)

    # Calculate shadow length
    # shadow_length = height / tan(altitude)
    shadow_length = height / np.tan(alt_rad)

    # Calculate shadow offset in x and y directions
    # Azimuth is measured from north clockwise
    # x offset = shadow_length * sin(azimuth)
    # y offset = shadow_length * cos(azimuth)
    dx = shadow_length * np.sin(az_rad)
    dy = shadow_length * np.cos(az_rad)

    # Get building coordinates
    coords = list(building_poly.exterior.coords)

    # Project each vertex
    shadow_coords = []
    for x, y in coords:
        # Shift coordinate in shadow direction
        shadow_x = x + dx
        shadow_y = y + dy
        shadow_coords.append((shadow_x, shadow_y))

    # Create shadow polygon by connecting original vertices to projected vertices
    # This creates a "side" of the shadow volume
    original_len = len(coords)

    # Combine original and projected vertices to create shadow polygon
    # The shadow polygon is the projection of the top vertices
    shadow_poly = Polygon(shadow_coords)

    return shadow_poly


def _shapely_to_geojson(geometry: Polygon) -> Dict[str, Any]:
    """
    Convert Shapely geometry to GeoJSON

    Args:
        geometry: Shapely geometry

    Returns:
        GeoJSON dictionary
    """
    if geometry.geom_type == "Polygon":
        coords = [list(geometry.exterior.coords)]
        # Add interiors if any
        for interior in geometry.interiors:
            coords.append(list(interior.coords))
        return {
            "type": "Polygon",
            "coordinates": coords
        }
    elif geometry.geom_type == "MultiPolygon":
        polygons = []
        for poly in geometry.geoms:
            polygons.append(_shapely_to_geojson(poly))
        return {
            "type": "MultiPolygon",
            "coordinates": [p["coordinates"] for p in polygons]
        }
    else:
        raise ValueError(f"Unsupported geometry type: {geometry.geom_type}")
