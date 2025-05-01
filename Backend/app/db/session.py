# Import SQLAlchemy components and context manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from models.variables import Base

# Database configuration
# SQLite database URL - points to the local SQLite database file
# Note: In production, consider using a more robust database like PostgreSQL
DATABASE_URL = "sqlite:///C:/Users/atvalabeishvili/Desktop/Projects/Qubdi-Tobias/VaraiblesTest.sqlite"

# Create SQLAlchemy engine
# This is the core interface to the database
engine = create_engine(
    DATABASE_URL,
    echo=False,              # Set to True to log all SQL statements (useful for debugging)
    future=True              # Use SQLAlchemy 2.x style API
)

# Create session factory
# This is used to create new database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,         # Disable auto-flush to have more control over when changes are committed
    autocommit=False,        # Disable auto-commit to use explicit transactions
    future=True             # Use SQLAlchemy 2.x style API
)

# Database initialization
# Drop and recreate all tables - WARNING: This will delete all existing data
# Only use this during development or when you want to reset the database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Declare base for models
# This is used as the base class for all SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Dependency function for FastAPI to get a database session.
    This function is used as a dependency in FastAPI route handlers.
    
    Yields:
        Session: A SQLAlchemy database session
        
    Note:
        The session is automatically closed after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    This can be used in scripts or tests to manage database sessions.
    
    Usage:
        with get_db_context() as db:
            # Use the database session
            result = db.query(Model).all()
    
    Yields:
        Session: A SQLAlchemy database session
        
    Note:
        The session is automatically closed when exiting the context.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

