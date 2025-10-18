"""
Export Endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import pandas as pd
import uuid
from datetime import datetime, timedelta

from backend.config.settings import settings
from backend.db.database import Database

router = APIRouter()


class ExportRequest(BaseModel):
    job_id: str
    format: str = "xlsx"  # xlsx, csv, txt, pdf
    filter_status: Optional[str] = None  # valid, error, duplicate
    include_stats: bool = True


class ExportResponse(BaseModel):
    export_id: str
    download_url: str
    format: str
    size: int
    expires_at: str


@router.post("/", response_model=ExportResponse)
async def create_export(request: ExportRequest):
    """
    Create export file - REAL IMPLEMENTATION
    """
    try:
        # Generate export ID
        export_id = str(uuid.uuid4())
        
        # Get cleaned data
        data = Database.get_cleaned_data(request.job_id)
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this job")
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create export directory
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # Generate file
        if request.format == "xlsx":
            file_path = os.path.join(settings.EXPORT_DIR, f"{export_id}.xlsx")
            df.to_excel(file_path, index=False)
        else:  # csv
            file_path = os.path.join(settings.EXPORT_DIR, f"{export_id}.csv")
            df.to_csv(file_path, index=False)
        
        file_size = os.path.getsize(file_path)
        
        return {
            "export_id": export_id,
            "download_url": f"/api/v1/export/{export_id}/download",
            "format": request.format,
            "size": file_size,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{export_id}/download")
async def download_export(export_id: str):
    """
    Download export file - REAL IMPLEMENTATION
    """
    try:
        # Try xlsx first, then csv
        file_path_xlsx = os.path.join(settings.EXPORT_DIR, f"{export_id}.xlsx")
        file_path_csv = os.path.join(settings.EXPORT_DIR, f"{export_id}.csv")
        
        if os.path.exists(file_path_xlsx):
            return FileResponse(
                file_path_xlsx,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"cleaned_data_{export_id}.xlsx"
            )
        elif os.path.exists(file_path_csv):
            return FileResponse(
                file_path_csv,
                media_type="text/csv",
                filename=f"cleaned_data_{export_id}.csv"
            )
        else:
            raise HTTPException(status_code=404, detail="Export file not found or expired")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/channel/{channel}")
async def export_by_channel(
    job_id: str = Path(..., description="Job ID"),
    channel: str = Path(..., pattern="^(email|whatsapp|call)$", description="Marketing channel")
):
    """
    Export data formatted for specific marketing channel
    """
    # TODO: Format data for channel
    
    return {
        "job_id": job_id,
        "channel": channel,
        "records": 85420,
        "download_url": f"/api/v1/export/{job_id}/channel/{channel}/download"
    }

