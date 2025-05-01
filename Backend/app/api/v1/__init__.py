# Initialize API routes
from fastapi import APIRouter

# Create the main API router
router = APIRouter()

# Import and include all endpoints
from .variables import router as variables_router

# Include all routers
router.include_router(variables_router)
