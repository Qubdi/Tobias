from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# SQL Server connection string using Windows Authentication
# DATABASE_URL = "sqlite:///C:/Users/Anri/Desktop/Qubdi/Qubdi-Tobias/VaraiblesTest.sqlite"
DATABASE_URL = "sqlite:///C:/Users/atvalabeishvili/Desktop/Projects/Qubdi-Tobias/VaraiblesTest.sqlite"


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,              # Set to True for SQL debugging
    future=True              # SQLAlchemy 2.x style
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Declare base for models
Base = declarative_base()

# Dependency for FastAPI or general DB access
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Context manager for scripts/tests
@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()