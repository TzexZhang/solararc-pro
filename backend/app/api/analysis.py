"""
Sunlight Analysis API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.building import Building
from app.schemas.analysis import (
    PointSunlightRequest,
    PointSunlightResponse,
    ShadowOverlapRequest,
    ShadowOverlapResponse
)
from app.services.solar_service import calculate_solar_position
from app.services.shadow_service import calculate_building_shadow
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/point-sunlight", response_model=dict)
async def analyze_point_sunlight(
    request: PointSunlightRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze effective sunlight duration for a specific point

    - **point**: {lat, lng} coordinates of the point to analyze
    - **date**: Analysis date in YYYY-MM-DD format (default: today)
    - **start_hour**: Start hour (default: 6)
    - **end_hour**: End hour (default: 18)

    Returns total sunlight hours and hourly breakdown
    """
    total_hours = request.end_hour - request.start_hour
    sunlight_hours = 0
    hourly_breakdown = []

    # Get buildings near the point (simplified - in production, use spatial query)
    # For now, we'll just check if the point has direct sunlight based on solar position
    # TODO: Implement actual shadow checking against building footprints

    for hour in range(request.start_hour, request.end_hour + 1):
        # Calculate solar position for this hour
        try:
            solar_pos = calculate_solar_position(
                request.point.lat,
                request.point.lng,
                request.date,
                hour,
                0
            )

            # Check if sun is above horizon
            is_sunny = solar_pos["solar_altitude"] > 0

            if is_sunny:
                sunlight_hours += 1

            hourly_breakdown.append({
                "hour": hour,
                "is_sunny": is_sunny,
                "blocked_by": None  # TODO: implement building shadow detection
            })

        except Exception as e:
            print(f"Error calculating solar position for hour {hour}: {str(e)}")
            hourly_breakdown.append({
                "hour": hour,
                "is_sunny": False,
                "blocked_by": None
            })

    sunlight_rate = sunlight_hours / total_hours if total_hours > 0 else 0

    return {
        "code": 200,
        "data": {
            "total_hours": total_hours,
            "sunlight_hours": round(sunlight_hours, 2),
            "sunlight_rate": round(sunlight_rate, 3),
            "hourly_breakdown": hourly_breakdown
        }
    }


@router.post("/shadow-overlap", response_model=dict)
async def analyze_shadow_overlap(
    request: ShadowOverlapRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze shadow overlap on target building from surrounding buildings

    - **target_building_id**: Building ID to analyze
    - **surrounding_building_ids**: List of surrounding building IDs
    - **date**: Analysis date in YYYY-MM-DD format (default: today)
    - **hour**: Hour (0-23, default: 12)

    Returns self-shadow area, projected shadow area, and overlap details
    """
    from app.api.shadows import calculate_shadow_overlap
    from geoalchemy2.shape import to_shape

    # Get target building
    target_building = db.query(Building).filter(Building.id == request.target_building_id).first()
    if not target_building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target building not found"
        )

    # Convert footprint to GeoJSON
    target_footprint_shape = to_shape(target_building.footprint)
    target_footprint_geojson = {
        "type": "Polygon",
        "coordinates": [list(target_footprint_shape.exterior.coords)]
    }

    # Get location
    centroid = target_footprint_shape.centroid
    lat = centroid.y
    lng = centroid.x

    # Calculate shadows for surrounding buildings
    surrounding_shadows = []

    for building_id in request.surrounding_building_ids:
        building = db.query(Building).filter(Building.id == building_id).first()
        if not building:
            continue

        try:
            from app.services.shadow_service import calculate_building_shadow

            building_footprint_shape = to_shape(building.footprint)
            building_footprint_geojson = {
                "type": "Polygon",
                "coordinates": [list(building_footprint_shape.exterior.coords)]
            }

            shadow_geojson, _ = calculate_building_shadow(
                building_footprint_geojson,
                float(building.total_height),
                lat,
                lng,
                request.date,
                request.hour,
                0
            )

            if shadow_geojson:
                surrounding_shadows.append(shadow_geojson)

        except Exception as e:
            print(f"Error calculating shadow for building {building_id}: {str(e)}")
            continue

    # Calculate overlap
    result = calculate_shadow_overlap(target_footprint_geojson, surrounding_shadows)

    return {
        "code": 200,
        "data": result
    }
