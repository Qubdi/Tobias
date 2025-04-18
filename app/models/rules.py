from sqlalchemy import Column, BigInteger, String, Float, REAL, Numeric
from app.db.session import Base

class Rules(Base):
    __tablename__ = "Rules"
    __table_args__ = {"schema": "dbo"}

    id = Column(BigInteger, primary_key=True, index=True)
    RuleName = Column(String(255), nullable=False)
    VariableId = Column(BigInteger, nullable=False)
    Allowed = Column(String(255), nullable=True)
    NotAllowed = Column(String(255), nullable=True)
    StartRange = Column(Float, nullable=True)  # VARCHAR type
    EndRange = Column(Float, nullable=True)    # VARCHAR type
    RuleValue = Column(String(255), nullable=True)
    RuleType = Column(String(255), nullable=True)

