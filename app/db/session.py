from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# SQL Server connection string using Windows Authentication
DATABASE_URL = (
    "mssql+pyodbc://@10.195.103.194/WH_Propensity"
    "?driver=SQL+Server&trusted_connection=yes"
)

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define Base once for all models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
