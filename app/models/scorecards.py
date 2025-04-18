from sqlalchemy import Column, BigInteger, String, Float, Boolean
from app.db.session import Base

class ScoreCards(Base):
    __tablename__ = "ScoreCard"
    __table_args__ = {"schema": "dbo"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ScoreCardId = Column(BigInteger, nullable=False)
    Name = Column(String(255), nullable=False)
    VariableId = Column(BigInteger, nullable=False)
    FixedValue = Column(String(255), nullable=True)
    StartRange = Column(Float, nullable=True)
    EndRange = Column(Float, nullable=True)
    SecondaryStartRange = Column(Float, nullable=True)
    SecondaryEndRange = Column(Float, nullable=True)
    Coefficient = Column(Float, nullable=True)
    Type = Column(String(255), nullable=True)
    IsExcel = Column(Boolean, nullable=True)
