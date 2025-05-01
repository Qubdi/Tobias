from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.v1 import router as variables_router  # Renamed to be more specific
from db.session import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Credit Scoring Engine API",
    description="API for managing and calculating credit scoring variables",
    version="1.0.0",
    docs_url="/api/docs",  # Removed /api prefix
    redoc_url="/api/redoc",  # Removed /api prefix
    openapi_url="/api/openapi.json"  # Removed /api prefix
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include variables router
app.include_router(variables_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_docs": "/api/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# python Backend/main.py

