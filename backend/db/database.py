"""
Database Helper - Simple SQLite Operations
"""
import sqlite3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

DB_FILE = "data_cleaning.db"

class Database:
    """Simple SQLite Database Helper"""
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        return sqlite3.connect(DB_FILE)
    
    @staticmethod
    def save_file(file_id: str, filename: str, path: str, size: int, rows: int, cols: int):
        """Save uploaded file info"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO files (id, filename, original_path, file_size, total_rows, total_columns)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (file_id, filename, path, size, rows, cols))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def create_job(job_id: str, file_id: str, settings: Dict):
        """Create cleaning job"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO jobs (id, file_id, status, progress, started_at, settings)
            VALUES (?, ?, 'processing', 0.0, ?, ?)
        """, (job_id, file_id, datetime.now().isoformat(), json.dumps(settings)))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_job_progress(job_id: str, progress: float, step: str, status: str = 'processing'):
        """Update job progress"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE jobs
            SET progress = ?, current_step = ?, status = ?
            WHERE id = ?
        """, (progress, step, status, job_id))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def complete_job(job_id: str):
        """Mark job as completed"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE jobs
            SET status = 'completed', progress = 1.0, completed_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), job_id))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_job(job_id: str) -> Optional[Dict]:
        """Get job details"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, file_id, status, progress, current_step, started_at, completed_at
            FROM jobs
            WHERE id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'job_id': row[0],
                'file_id': row[1],
                'status': row[2],
                'progress': row[3],
                'current_step': row[4],
                'started_at': row[5],
                'completed_at': row[6]
            }
        return None
    
    @staticmethod
    def make_json_serializable(obj):
        """Convert any type to JSON-serializable format - FLEXIBLE FOR ANY FILE TYPE"""
        import pandas as pd
        import numpy as np
        from datetime import datetime, date, timedelta
        
        if isinstance(obj, dict):
            return {k: Database.make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [Database.make_json_serializable(item) for item in obj]
        elif isinstance(obj, (pd.Timestamp, datetime, date)):
            return obj.isoformat() if pd.notna(obj) else ""
        elif isinstance(obj, timedelta):
            return str(obj)
        elif isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.to_list()
        elif isinstance(obj, bool):
            return obj
        elif pd.isna(obj) or obj is None:
            return ""
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='ignore')
        else:
            try:
                return str(obj) if obj != "" else ""
            except:
                return ""
    
    @staticmethod
    def save_results(job_id: str, results: List[Dict]):
        """Save cleaning results - HANDLES ANY DATA TYPE"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        for idx, result in enumerate(results):
            # ✅ Make everything JSON-serializable
            original_data = Database.make_json_serializable(result.get('original', {}))
            cleaned_data = Database.make_json_serializable(result.get('cleaned', {}))
            errors = result.get('errors', [])
            
            cursor.execute("""
                INSERT INTO results (job_id, row_index, original_data, cleaned_data, status, errors)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                job_id,
                idx,
                json.dumps(original_data, ensure_ascii=False),
                json.dumps(cleaned_data, ensure_ascii=False),
                result.get('status', 'valid'),
                json.dumps(errors, ensure_ascii=False)
            ))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def save_statistics(job_id: str, stats: Dict):
        """Save job statistics"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO statistics (job_id, total_rows, valid_rows, error_rows, duplicate_rows, valid_phones, valid_emails, classified_rows, quality_score, processing_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            stats.get('total_rows', 0),
            stats.get('valid_rows', 0),
            stats.get('error_rows', 0),
            stats.get('duplicate_rows', 0),
            stats.get('valid_phones', 0),
            stats.get('valid_emails', 0),
            stats.get('classified_rows', 0),
            stats.get('quality_score', 0.0),
            stats.get('processing_time', 0)
        ))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_statistics(job_id: str) -> Optional[Dict]:
        """Get job statistics"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_rows, valid_rows, error_rows, duplicate_rows, valid_phones, valid_emails, classified_rows, quality_score, processing_time
            FROM statistics
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'job_id': job_id,
                'total_rows': row[0],
                'valid_rows': row[1],
                'error_rows': row[2],
                'duplicate_rows': row[3],
                'valid_phones': row[4],
                'valid_emails': row[5],
                'classified_rows': row[6],
                'quality_score': row[7],
                'processing_time': row[8],
                'completed_at': datetime.now().isoformat()
            }
        return None
    
    @staticmethod
    def get_results_preview(job_id: str, page: int = 1, page_size: int = 50) -> Dict:
        """Get paginated results preview"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        offset = (page - 1) * page_size
        
        cursor.execute("""
            SELECT row_index, original_data, cleaned_data, status, errors
            FROM results
            WHERE job_id = ?
            ORDER BY row_index
            LIMIT ? OFFSET ?
        """, (job_id, page_size, offset))
        
        rows = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM results WHERE job_id = ?", (job_id,))
        total = cursor.fetchone()[0]
        
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'index': row[0],
                'data': json.loads(row[2]),  # cleaned_data
                'status': row[3],
                'errors': json.loads(row[4]) if row[4] else []
            })
        
        return {
            'job_id': job_id,
            'total_rows': total,
            'data': data,
            'page': page,
            'page_size': page_size,
            'has_more': offset + page_size < total
        }
    
    @staticmethod
    def get_file_path(file_id: str) -> Optional[str]:
        """Get file path by file_id"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT original_path FROM files WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    @staticmethod
    def get_cleaned_data(job_id: str) -> List[Dict]:
        """Get all cleaned data for export"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cleaned_data
            FROM results
            WHERE job_id = ?
            ORDER BY row_index
        """, (job_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]

