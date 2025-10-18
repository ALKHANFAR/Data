"""
Results Endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from backend.db.database import Database

router = APIRouter()


class ResultsSummary(BaseModel):
    job_id: str
    total_rows: int
    valid_rows: int
    error_rows: int
    duplicate_rows: int
    valid_phones: int
    valid_emails: int
    classified_rows: int
    quality_score: float
    processing_time: int
    completed_at: str


class ResultRow(BaseModel):
    index: int
    data: Dict[str, Any]
    status: str
    errors: List[str]


class ResultsPreview(BaseModel):
    job_id: str
    total_rows: int
    data: List[ResultRow]
    page: int
    page_size: int
    has_more: bool


@router.get("/{job_id}/summary", response_model=ResultsSummary)
async def get_results_summary(job_id: str):
    """
    Get cleaning results summary - REAL IMPLEMENTATION
    """
    try:
        stats = Database.get_statistics(job_id)
        
        if not stats:
            raise HTTPException(status_code=404, detail="Results not found")
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/preview", response_model=ResultsPreview)
async def get_results_preview(
    job_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=10, le=100),
    filter_status: Optional[str] = Query(None, regex="^(valid|error|duplicate)$")
):
    """
    Get paginated results preview - REAL IMPLEMENTATION
    """
    try:
        results = Database.get_results_preview(job_id, page, page_size)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/stats")
async def get_detailed_stats(job_id: str):
    """
    Get detailed statistics
    """
    # TODO: Calculate from results
    
    return {
        "job_id": job_id,
        "total_records": 100000,
        "quality_breakdown": {
            "excellent": 65420,
            "good": 20000,
            "medium": 8580,
            "poor": 6000
        },
        "error_categories": {
            "invalid_phone": 5420,
            "invalid_email": 3820,
            "missing_data": 2140,
            "duplicate": 2200
        },
        "country_distribution": {
            "السعودية": 65000,
            "الإمارات": 20000,
            "الكويت": 10000,
            "قطر": 5000
        },
        "phone_types": {
            "mobile": 82000,
            "landline": 8000,
            "invalid": 10000
        }
    }

