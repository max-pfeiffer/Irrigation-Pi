"""API routers for API version 1.0."""
from fastapi import APIRouter

from app.api.v1.endpoints import schedule

api_router = APIRouter()
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
