from fastapi import FastAPI
import uvicorn
from routers.v1.variables import  router as variables_router  # Import your variables router
from db.session import engine, Base  # your database engine

# Create all tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI app with metadata
app = FastAPI(
    title="Credit Scoring Engine API",  # App title for Swagger UI
    version="1.0"                        # API version
)

# Register the variables router under versioned API path
app.include_router(
    variables_router,
    prefix="/routers/v1",        # Full path will be /routers/v1/variables
    tags=["Variables"]       # Swagger UI grouping
)

# Root health check / welcome endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Credit Scoring Engine API!"}

# Proper entry point check
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# python Backend/main.py

