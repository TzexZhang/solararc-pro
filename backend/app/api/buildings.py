"""
Building Data API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from geoalchemy2.functions import ST_Intersects, ST_MakeEnvelope
from geoalchemy2.shape import to_shape

from app.database import get_db
from app.models.building import Building
from app.schemas.building import BuildingResponse, BuildingCreate, BuildingListResponse
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/bbox", response_model=dict)
async def get_buildings_in_bbox(
    min_lat: float = Query(..., ge=-90, le=90, description="Minimum latitude"),
    max_lat: float = Query(..., ge=-90, le=90, description="Maximum latitude"),
    min_lng: float = Query(..., ge=-180, le=180, description="Minimum longitude"),
    max_lng: float = Query(..., ge=-180, le=180, description="Maximum longitude"),
    db: Session = Depends(get_db)
):
    """
    Get buildings within a bounding box

    Returns all buildings whose footprint intersects with the specified bounding box.
    """
    try:
        from sqlalchemy import text

        # MySQL 8.0: Extract coordinates and compare numerically since ST_MakeEnvelope doesn't support geographic SRID
        # MySQL spatial functions use (lat, lng) format for all geometry types
        sql = f"""
            SELECT id, name, building_type, total_height, floor_area, floor_count,
                   reflective_rate, address, district, city,
                   ST_AsGeoJSON(footprint) as footprint,
                   created_at, updated_at
            FROM buildings
            WHERE MBRIntersects(
                footprint,
                ST_GeomFromText('POLYGON(({min_lat} {min_lng}, {min_lat} {max_lng}, {max_lat} {max_lng}, {max_lat} {min_lng}, {min_lat} {min_lng}))', 4326)
            )
        """

        result = db.execute(text(sql))

        building_responses = []
        for row in result:
            import json
            footprint_geojson = json.loads(row[10]) if row[10] else None

            building_responses.append({
                "id": row[0],
                "name": row[1],
                "building_type": row[2],
                "total_height": float(row[3]),
                "floor_area": float(row[4]) if row[4] else None,
                "floor_count": row[5],
                "reflective_rate": float(row[6]),
                "address": row[7],
                "district": row[8],
                "city": row[9],
                "footprint": footprint_geojson,
                "created_at": row[11].isoformat() if row[11] else None,
                "updated_at": row[12].isoformat() if row[12] else None
            })

        return {
            "code": 200,
            "data": {
                "buildings": building_responses,
                "total": len(building_responses)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch buildings: {str(e)}"
        )


@router.get("/{building_id}", response_model=dict)
async def get_building(building_id: str, db: Session = Depends(get_db)):
    """
    Get building details by ID
    """
    building = db.query(Building).filter(Building.id == building_id).first()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )

    # Convert footprint to GeoJSON
    footprint_shape = to_shape(building.footprint)
    footprint_geojson = {
        "type": "Polygon",
        "coordinates": [list(footprint_shape.exterior.coords)]
    }

    return {
        "code": 200,
        "data": {
            "id": building.id,
            "name": building.name,
            "building_type": building.building_type,
            "footprint": footprint_geojson,
            "total_height": float(building.total_height),
            "floor_area": float(building.floor_area) if building.floor_area else None,
            "floor_count": building.floor_count,
            "reflective_rate": float(building.reflective_rate),
            "address": building.address,
            "district": building.district,
            "city": building.city,
            "created_at": building.created_at.isoformat(),
            "updated_at": building.updated_at.isoformat()
        }
    }


@router.post("/import", response_model=dict)
async def import_buildings(
    buildings_data: List[BuildingCreate],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Import building data

    Accepts a list of building objects with GeoJSON footprints.
    """
    success_count = 0
    failed_count = 0
    errors = []

    for building_data in buildings_data:
        try:
            # Convert GeoJSON to WKT for database storage
            from app.core.utils import geojson_to_wkt
            from sqlalchemy import func

            wkt = geojson_to_wkt(building_data.footprint)

            # Create building
            new_building = Building(
                name=building_data.name,
                building_type=building_data.building_type,
                footprint=func.ST_GeomFromText(wkt, 4326),
                total_height=building_data.total_height,
                floor_area=building_data.floor_area,
                floor_count=building_data.floor_count,
                reflective_rate=building_data.reflective_rate,
                address=building_data.address,
                district=building_data.district,
                city=building_data.city,
                country=building_data.country
            )

            db.add(new_building)
            success_count += 1

        except Exception as e:
            failed_count += 1
            errors.append({
                "building": building_data.name if building_data.name else "unknown",
                "error": str(e)
            })

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save buildings: {str(e)}"
        )

    return {
        "code": 201,
        "data": {
            "success_count": success_count,
            "failed_count": failed_count,
            "errors": errors
        }
    }


@router.delete("/{building_id}", response_model=dict)
async def delete_building(
    building_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a building by ID
    """
    building = db.query(Building).filter(Building.id == building_id).first()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )

    db.delete(building)
    db.commit()

    return {
        "code": 200,
        "message": "Building deleted successfully"
    }
