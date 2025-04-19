from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Variable(Base):
    __tablename__ = 'variables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    calculation_type = Column(String(10), nullable=False)  # 'live', 'dwh', 'hybrid'
    is_active = Column(Boolean, default=True)
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    versions = relationship('VariableVersion', back_populates='variable', cascade="all, delete-orphan")
    results = relationship('VariableResult', back_populates='variable', cascade="all, delete-orphan")


class VariableVersion(Base):
    __tablename__ = 'variable_versions'

    id = Column(Integer, primary_key=True)
    variable_id = Column(Integer, ForeignKey('variables.id'), nullable=False)
    version_number = Column(Integer, nullable=False)
    sql_script = Column(Text, nullable=False)
    change_reason = Column(Text)
    edited_by = Column(String(50))
    edited_at = Column(DateTime, default=datetime.utcnow)

    variable = relationship('Variable', back_populates='versions')

    __table_args__ = (UniqueConstraint('variable_id', 'version_number', name='uq_variable_version'),)


class VariableResult(Base):
    __tablename__ = 'variable_results'

    id = Column(Integer, primary_key=True)
    application_id = Column(String(50), nullable=False)
    variable_id = Column(Integer, ForeignKey('variables.id'), nullable=False)
    value = Column(Text)
    calculated_by = Column(String(50))
    calculated_at = Column(DateTime, default=datetime.utcnow)

    variable = relationship('Variable', back_populates='results')

    __table_args__ = (UniqueConstraint('application_id', 'variable_id', name='uq_app_variable'),)


class VariableExecution(Base):
    __tablename__ = 'variable_executions'

    id = Column(Integer, primary_key=True)
    application_id = Column(String(50), nullable=False)
    variable_id = Column(Integer, ForeignKey('variables.id'))
    executed_by = Column(String(50))
    result = Column(Text)
    executed_at = Column(DateTime, default=datetime.utcnow)
