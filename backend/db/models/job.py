"""
Cleaning Job Model
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.db.base import Base


class CleaningJob(Base):
    __tablename__ = "cleaning_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)
    current_step = Column(String)
    settings = Column(JSON)
    
    # Statistics
    total_rows = Column(Integer)
    processed_rows = Column(Integer, default=0)
    valid_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)
    duplicate_rows = Column(Integer, default=0)
    quality_score = Column(Float)
    
    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    processing_time = Column(Integer)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    file = relationship("UploadedFile", backref="jobs")
    user = relationship("User", backref="jobs")

