# Initialize API version 1 routes
from fastapi import APIRouter

router = APIRouter()

# Import individual routers
from .rules import router as rules_router
from .variables import router as variables_router
from .scorecards import router as scorecards_router

# Include routers
router.include_router(rules_router, prefix="/rules", tags=["Rules"])

router.include_router(variables_router, prefix="/variables", tags=["Variables"])

router.include_router(scorecards_router, prefix="/scorecards", tags=["Scorecards"])