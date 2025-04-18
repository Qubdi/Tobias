from fastapi import FastAPI
from app.api.v1.rules import router as rules_router
from app.api.v1.variables import router as variables_router
from app.api.v1.scorecards import router as scorecards_router

app = FastAPI(title="Credit Scoring Engine API", version="1.0")

# Include API routers
app.include_router(rules_router, prefix="/api/v1", tags=["Rules"])
app.include_router(variables_router, prefix="/api/v1", tags=["Variables"])
app.include_router(scorecards_router,  prefix="/api/v1", tags=["Scorecards"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Credit Scoring Engine API!"}
