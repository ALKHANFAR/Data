"""
Setup Database - Initialize SQLite Database with Tables
"""
import sqlite3
import os

DB_FILE = "data_cleaning.db"

def create_database():
    """Create SQLite database with all required tables"""
    
    # Remove old database if exists
    if os.path.exists(DB_FILE):
        print(f"⚠️  Removing old database: {DB_FILE}")
        os.remove(DB_FILE)
    
    # Create new database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("🔨 Creating tables...")
    
    # Files table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            original_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            total_rows INTEGER NOT NULL,
            total_columns INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'uploaded'
        )
    """)
    print("✅ Created 'files' table")
    
    # Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            file_id TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            progress REAL DEFAULT 0.0,
            current_step TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            settings TEXT,
            FOREIGN KEY (file_id) REFERENCES files(id)
        )
    """)
    print("✅ Created 'jobs' table")
    
    # Results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            row_index INTEGER NOT NULL,
            original_data TEXT NOT NULL,
            cleaned_data TEXT NOT NULL,
            status TEXT NOT NULL,
            errors TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)
    print("✅ Created 'results' table")
    
    # Statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL UNIQUE,
            total_rows INTEGER DEFAULT 0,
            valid_rows INTEGER DEFAULT 0,
            error_rows INTEGER DEFAULT 0,
            duplicate_rows INTEGER DEFAULT 0,
            valid_phones INTEGER DEFAULT 0,
            valid_emails INTEGER DEFAULT 0,
            classified_rows INTEGER DEFAULT 0,
            quality_score REAL DEFAULT 0.0,
            processing_time INTEGER DEFAULT 0,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)
    print("✅ Created 'statistics' table")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Database '{DB_FILE}' created successfully!")
    print(f"📊 Location: {os.path.abspath(DB_FILE)}")
    
if __name__ == "__main__":
    create_database()

