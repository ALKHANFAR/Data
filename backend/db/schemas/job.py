"""
Job Schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class JobBase(BaseModel):
    settings: Dict


class JobCreate(JobBase):
    job_id: str
    file_id: int
    user_id: int


class JobUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[float] = None
    current_step: Optional[str] = None
    processed_rows: Optional[int] = None
    valid_rows: Optional[int] = None
    error_rows: Optional[int] = None
    duplicate_rows: Optional[int] = None
    quality_score: Optional[float] = None


class JobInDB(JobBase):
    id: int
    job_id: str
    file_id: int
    user_id: int
    status: str
    progress: float
    current_step: Optional[str]
    total_rows: Optional[int]
    processed_rows: int
    valid_rows: int
    error_rows: int
    duplicate_rows: int
    quality_score: Optional[float]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    processing_time: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class Job(JobInDB):
    pass

