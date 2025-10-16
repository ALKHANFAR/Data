"""
Helper Functions
"""
import os
import hashlib
from typing import Optional


def get_file_hash(filepath: str) -> str:
    """Get MD5 hash of file"""
    hash_md5 = hashlib.md5()
    
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    
    return hash_md5.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"


def safe_filename(filename: str) -> str:
    """Make filename safe"""
    # Remove dangerous characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    
    return "".join(c if c in safe_chars else "_" for c in filename)

