"""
File Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    filename: str


class FileCreate(FileBase):
    file_id: str
    file_path: str
    file_size: int
    rows_count: Optional[int] = None
    columns_count: Optional[int] = None


class FileInDB(FileBase):
    id: int
    file_id: str
    user_id: int
    file_size: int
    rows_count: Optional[int]
    columns_count: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class File(FileInDB):
    pass

