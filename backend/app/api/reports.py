"""
Analysis Reports API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from app.database import get_db
from app.models.user import User
from app.models.analysis_report import AnalysisReport, AnalysisType
from app.models.building_score import BuildingScore
from app.schemas.analysis import PointSunlightRequest
from app.services.report_service import (
    create_analysis_report,
    generate_building_scores,
    export_report_to_pdf
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/analysis/reports", tags=["Analysis Reports"])


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_report(
    project_id: Optional[str] = None,
    name: str = Query(..., description="Report name"),
    analysis_type: AnalysisType = Query(..., description="Analysis type"),
    latitude: float = Query(..., ge=-90, le=90, description="Center latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Center longitude"),
    date_start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    date_end: str = Query(..., description="End date (YYYY-MM-DD)"),
    building_ids: List[str] = Query(..., description="List of building IDs"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new analysis report

    - **project_id**: Optional project ID
    - **name**: Report name
    - **analysis_type**: Type of analysis (daily, seasonal, custom)
    - **latitude**: Center latitude for analysis
    - **longitude**: Center longitude for analysis
    - **date_start**: Start date in YYYY-MM-DD format
    - **date_end**: End date in YYYY-MM-DD format
    - **building_ids**: List of building IDs to analyze
    """
    try:
        # Parse dates
        start_date = date.fromisoformat(date_start)
        end_date = date.fromisoformat(date_end)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    # Create report
    report = create_analysis_report(
        user_id=current_user.id,
        project_id=project_id,
        name=name,
        analysis_type=analysis_type,
        latitude=latitude,
        longitude=longitude,
        date_start=start_date,
        date_end=end_date,
        building_ids=building_ids,
        db=db
    )

    return {
        "code": 201,
        "data": {
            "id": report.id,
            "name": report.name,
            "status": "processing",
            "created_at": report.created_at.isoformat()
        }
    }


@router.get("", response_model=dict)
async def get_reports(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of analysis reports for current user

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **project_id**: Optional filter by project ID
    """
    # Build query
    query = db.query(AnalysisReport).filter(AnalysisReport.user_id == current_user.id)

    if project_id:
        query = query.filter(AnalysisReport.project_id == project_id)

    # Get total count
    total = query.count()

    # Paginate
    offset = (page - 1) * page_size
    reports = query.order_by(AnalysisReport.created_at.desc()).offset(offset).limit(page_size).all()

    # Convert to response format
    report_list = []
    for report in reports:
        report_list.append({
            "id": report.id,
            "name": report.name,
            "analysis_type": report.analysis_type.value,
            "total_sunlight_hours": float(report.total_sunlight_hours) if report.total_sunlight_hours else None,
            "avg_shadow_coverage": float(report.avg_shadow_coverage) if report.avg_shadow_coverage else None,
            "building_count": report.building_count,
            "created_at": report.created_at.isoformat(),
            "updated_at": report.updated_at.isoformat()
        })

    return {
        "code": 200,
        "data": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "reports": report_list
        }
    }


@router.get("/{report_id}", response_model=dict)
async def get_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analysis report details by ID
    """
    report = db.query(AnalysisReport).filter(
        AnalysisReport.id == report_id,
        AnalysisReport.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Parse results JSON
    import json
    results = json.loads(report.results) if report.results else {}

    return {
        "code": 200,
        "data": {
            "id": report.id,
            "name": report.name,
            "analysis_type": report.analysis_type.value,
            "latitude": float(report.latitude),
            "longitude": float(report.longitude),
            "date_start": report.date_start.isoformat(),
            "date_end": report.date_end.isoformat(),
            "total_sunlight_hours": float(report.total_sunlight_hours) if report.total_sunlight_hours else None,
            "avg_shadow_coverage": float(report.avg_shadow_coverage) if report.avg_shadow_coverage else None,
            "building_count": report.building_count,
            "results": results,
            "report_file_path": report.report_file_path,
            "created_at": report.created_at.isoformat(),
            "updated_at": report.updated_at.isoformat()
        }
    }


@router.get("/{report_id}/building-scores", response_model=dict)
async def get_building_scores(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get building daylight scores for a report
    """
    # Verify report ownership
    report = db.query(AnalysisReport).filter(
        AnalysisReport.id == report_id,
        AnalysisReport.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Get scores
    scores = db.query(BuildingScore).filter(BuildingScore.report_id == report_id).all()

    building_scores = []
    for score in scores:
        # Get building name
        from app.models.building import Building
        building = db.query(Building).filter(Building.id == score.building_id).first()
        building_name = building.name if building else "Unknown"

        building_scores.append({
            "building_id": score.building_id,
            "building_name": building_name,
            "overall_score": score.overall_score,
            "grade": score.grade.value,
            "avg_sunlight_hours": float(score.avg_sunlight_hours) if score.avg_sunlight_hours else None,
            "peak_sunlight_hours": float(score.peak_sunlight_hours) if score.peak_sunlight_hours else None,
            "continuous_sunlight_hours": float(score.continuous_sunlight_hours) if score.continuous_sunlight_hours else None,
            "shadow_frequency": score.shadow_frequency,
            "shading_buildings": score.shading_buildings
        })

    return {
        "code": 200,
        "data": {
            "report_id": report_id,
            "buildings": building_scores
        }
    }


@router.get("/{report_id}/export", response_model=dict)
async def export_report(
    report_id: str,
    format: str = Query("pdf", description="Export format: pdf, excel, csv"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export analysis report to file

    - **format**: Export format (pdf, excel, csv)
    """
    # Verify report ownership
    report = db.query(AnalysisReport).filter(
        AnalysisReport.id == report_id,
        AnalysisReport.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if format == "pdf":
        try:
            filepath = export_report_to_pdf(report_id, db)

            return {
                "code": 200,
                "data": {
                    "format": "pdf",
                    "file_path": filepath,
                    "download_url": f"/api/v1/analysis/reports/{report_id}/download"
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate PDF: {str(e)}"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format '{format}' not yet supported"
        )


@router.delete("/{report_id}", response_model=dict)
async def delete_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an analysis report
    """
    report = db.query(AnalysisReport).filter(
        AnalysisReport.id == report_id,
        AnalysisReport.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()

    return {
        "code": 200,
        "message": "Report deleted successfully"
    }
