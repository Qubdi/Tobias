"""
Main application file for the Credit Scoring Engine API.
This file sets up the FastAPI application, configures middleware, and defines the main entry point.
"""

# Import required FastAPI components and other dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.v1 import router as variables_router  # Import the variables router from API v1
from db.session import engine, Base

# Initialize FastAPI application with comprehensive metadata
# This configuration sets up the API documentation and versioning
app = FastAPI(
    title="Credit Scoring Engine API",
    description="API for managing and calculating credit scoring variables",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI documentation endpoint
    redoc_url="/api/redoc",  # ReDoc documentation endpoint
    openapi_url="/api/openapi.json"  # OpenAPI schema endpoint
)

# Configure Cross-Origin Resource Sharing (CORS)
# This middleware allows the API to be accessed from different origins
# Note: In production, replace "*" with specific allowed origins for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (configure for production)
    allow_credentials=True,  # Allows cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include the variables router
# This mounts all the variable-related endpoints under the API
app.include_router(variables_router)

# Health check endpoint
# This endpoint provides basic API status information
@app.get("/health")
async def health_check():
    """
    Health check endpoint that returns the current status of the API.
    
    Returns:
        dict: A dictionary containing:
            - status: Current health status
            - version: API version
            - api_docs: URL to API documentation
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_docs": "/api/docs"
    }

# Application entry point
# This block runs when the script is executed directly
if __name__ == "__main__":
    # Start the Uvicorn server with development settings
    uvicorn.run(
        "main:app",  # Module and application name
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,  # Default port
        reload=True,  # Enable auto-reload during development
        log_level="info"  # Set logging level
    )

# To run the application:
# python Backend/main.py

