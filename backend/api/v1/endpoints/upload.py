"""
File Upload Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import os
import uuid
import pandas as pd
from datetime import datetime

from backend.config.settings import settings

router = APIRouter()


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    rows: int
    columns: int
    uploaded_at: str
    status: str


class GoogleSheetsRequest(BaseModel):
    url: HttpUrl


@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload Excel or CSV file
    """
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Read file to get info
    try:
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:  # CSV
            df = pd.read_csv(file_path)
        
        rows = len(df)
        columns = len(df.columns)
    except Exception as e:
        # Clean up file
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read file: {str(e)}"
        )
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": file_size,
        "rows": rows,
        "columns": columns,
        "uploaded_at": datetime.now().isoformat(),
        "status": "uploaded"
    }


@router.post("/google-sheets", response_model=UploadResponse)
async def upload_google_sheets(request: GoogleSheetsRequest):
    """
    Import from Google Sheets
    """
    try:
        # Extract sheet ID from URL
        url_str = str(request.url)
        if '/d/' in url_str:
            sheet_id = url_str.split('/d/')[1].split('/')[0]
        else:
            raise ValueError("Invalid Google Sheets URL")
        
        # Convert to export URL
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        # Read data
        df = pd.read_csv(export_url)
        
        # Generate file ID
        file_id = str(uuid.uuid4())
        
        # Save as CSV
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.csv")
        df.to_csv(file_path, index=False)
        
        file_size = os.path.getsize(file_path)
        
        return {
            "file_id": file_id,
            "filename": "google_sheets_import.csv",
            "size": file_size,
            "rows": len(df),
            "columns": len(df.columns),
            "uploaded_at": datetime.now().isoformat(),
            "status": "uploaded"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to import Google Sheets: {str(e)}"
        )


@router.get("/{file_id}")
async def get_file_info(file_id: str):
    """Get uploaded file info"""
    # TODO: Get from database
    return {
        "file_id": file_id,
        "filename": "example.xlsx",
        "status": "uploaded"
    }


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete uploaded file"""
    # Find file
    for ext in ['.xlsx', '.xls', '.csv', '.txt']:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": "File deleted successfully"}
    
    raise HTTPException(status_code=404, detail="File not found")

