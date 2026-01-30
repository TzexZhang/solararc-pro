"""
Shadow Calculation API Routes
"""
import time
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.building import Building
from app.schemas.analysis import (
    ShadowCalculationRequest,
    ShadowCalculationResponse,
    ShadowOverlapRequest,
    ShadowOverlapResponse,
    ShadowComparisonResponse
)
from app.services.shadow_service import (
    calculate_building_shadow,
    calculate_shadow_overlap,
    calculate_shadow_comparison
)
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/shadows", tags=["Shadows"])


@router.post("/calculate", response_model=dict)
async def calculate_shadows(
    request: ShadowCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate shadows for buildings

    - **building_ids**: List of building IDs
    - **date**: Analysis date in YYYY-MM-DD format (default: today)
    - **hour**: Hour (0-23, default: 12)
    - **minute**: Minute (0-59, default: 0)
    """
    start_time = time.time()

    shadows = []

    for building_id in request.building_ids:
        # Get building from database
        building = db.query(Building).filter(Building.id == building_id).first()

        if not building:
            continue

        try:
            # Convert footprint to GeoJSON
            from geoalchemy2.shape import to_shape
            footprint_shape = to_shape(building.footprint)
            footprint_geojson = {
                "type": "Polygon",
                "coordinates": [list(footprint_shape.exterior.coords)]
            }

            # Get center coordinates
            centroid = footprint_shape.centroid
            lat = centroid.y
            lng = centroid.x

            # Calculate shadow
            shadow_geojson, shadow_area = calculate_building_shadow(
                footprint_geojson,
                float(building.total_height),
                lat,
                lng,
                request.date,
                request.hour,
                request.minute
            )

            if shadow_geojson:
                shadows.append({
                    "building_id": building_id,
                    "shadow_polygon": shadow_geojson,
                    "area": shadow_area
                })

        except Exception as e:
            # Log error but continue processing other buildings
            print(f"Error calculating shadow for building {building_id}: {str(e)}")
            continue

    calculation_time_ms = int((time.time() - start_time) * 1000)

    return {
        "code": 200,
        "data": {
            "shadows": shadows,
            "calculation_time_ms": calculation_time_ms
        }
    }


@router.post("/overlap", response_model=dict)
async def get_shadow_overlap(
    request: ShadowOverlapRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate shadow overlap on target building

    - **target_building_id**: Building ID to analyze
    - **surrounding_building_ids**: List of surrounding building IDs
    - **date**: Analysis date in YYYY-MM-DD format (default: today)
    - **hour**: Hour (0-23, default: 12)
    """
    # Get target building
    target_building = db.query(Building).filter(Building.id == request.target_building_id).first()
    if not target_building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target building not found"
        )

    # Convert target building footprint to GeoJSON
    from geoalchemy2.shape import to_shape
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


@router.get("/compare-extremes", response_model=dict)
async def compare_shadow_extremes(
    building_id: str,
    hour: int = 12,
    db: Session = Depends(get_db)
):
    """
    Compare shadows on winter solstice vs summer solstice

    - **building_id**: Building ID to analyze
    - **hour**: Hour to compare (default: 12, solar noon)

    Returns shadow comparison showing the difference between the longest
    and shortest shadows of the year.
    """
    # Get building
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )

    # Convert footprint to GeoJSON
    from geoalchemy2.shape import to_shape
    footprint_shape = to_shape(building.footprint)
    footprint_geojson = {
        "type": "Polygon",
        "coordinates": [list(footprint_shape.exterior.coords)]
    }

    # Get location
    centroid = footprint_shape.centroid
    lat = centroid.y
    lng = centroid.x

    # Calculate comparison
    result = calculate_shadow_comparison(
        footprint_geojson,
        float(building.total_height),
        lat,
        lng,
        hour
    )

    return {
        "code": 200,
        "data": result
    }
