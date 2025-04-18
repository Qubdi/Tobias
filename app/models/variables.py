from sqlalchemy import Column, BigInteger, String
from app.db.session import Base

class Variables(Base):
    __tablename__ = "Variables"
    __table_args__ = {"schema": "dbo"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    VariableName = Column(String(255), nullable=False)
    Logic = Column(String(255), nullable=True)
    VariableType = Column(String(255), nullable=True)
    DBType = Column(String(255), nullable=True)
