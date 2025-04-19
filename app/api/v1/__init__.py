# Initialize API version 1 routes
from fastapi import APIRouter

router = APIRouter()

# Import individual routers
from .variables import router as variables_router


# Include routers
router.include_router(variables_router, prefix="/variables", tags=["Variables"])

