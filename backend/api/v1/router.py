"""
Main API Router
"""
from fastapi import APIRouter
from backend.api.v1.endpoints import auth, upload, cleaning, results, export

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(cleaning.router, prefix="/clean", tags=["Cleaning"])
api_router.include_router(results.router, prefix="/results", tags=["Results"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])

