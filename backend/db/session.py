"""
Database Session Management
"""
from backend.db.base import SessionLocal, engine, Base


def init_db():
    """Initialize database"""
    # Import all models here
    # from backend.db.models import user, file, job
    
    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get database session"""
    return SessionLocal()

