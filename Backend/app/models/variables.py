from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy import   UniqueConstraint, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship, declarative_base, Mapped
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

from schemas.variables import CalculationType


# Create the declarative base class for all models
# This is used as the base class for all SQLAlchemy models in the application
Base = declarative_base()


class Variable(Base):
    """
    Represents a credit scoring variable in the database.
    
    This is the main model for storing credit scoring variables. Each variable can have
    multiple versions (SQL scripts) and multiple calculation results.
    
    Attributes:
        id: Unique identifier
        name: Unique name of the variable
        description: Description of the variable's purpose
        calculation_type: Type of calculation (live/dwh/hybrid)
        is_active: Whether the variable is active
        created_by: User who created the variable
        created_at: Timestamp when the variable was created
        updated_at: Timestamp when the variable was last updated
        versions: List of variable versions
        results: List of calculation results
        additional_metadata: Additional metadata for the variable
    """
    __tablename__ = 'variables'

    # Primary key with index for faster lookups
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    
    # Unique name constraint ensures no duplicate variable names
    name: Mapped[str] = Column(String(255), unique=True, nullable=False)
    
    # Optional description field for documenting the variable's purpose
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    
    # Calculation type using SQL enum for type safety
    # This determines how the variable is calculated (live, dwh, or hybrid)
    calculation_type: Mapped[str] = Column(
        SQLEnum(CalculationType, name='calculation_type_enum'),
        nullable=False
    )
    
    # Soft delete flag - allows for logical deletion without removing data
    is_active: Mapped[bool] = Column(Boolean, default=True)
    
    # Audit fields for tracking creation and updates
    created_by: Mapped[Optional[str]] = Column(String(255), nullable=True)
    updated_by: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Flexible metadata storage for future extensibility
    additional_metadata: Mapped[Optional[dict]] = Column(JSON, nullable=True)

    # Relationships with cascade delete for referential integrity
    # When a variable is deleted, all its versions and results are also deleted
    versions: Mapped[List['VariableVersion']] = relationship(
        'VariableVersion', 
        back_populates='variable',
        cascade="all, delete-orphan"  # Delete versions when variable is deleted
    )
    results: Mapped[List['VariableResult']] = relationship(
        'VariableResult',
        back_populates='variable',
        cascade="all, delete-orphan"  # Delete results when variable is deleted
    )


class VariableVersion(Base):
    """
    Represents a version of a variable's SQL script.
    
    This model tracks different versions of SQL scripts for each variable,
    allowing for version control and history tracking.
    
    Attributes:
        id: Unique identifier
        variable_id: ID of the parent variable
        version_number: Version number of the SQL script
        sql_script: The SQL script for calculation
        change_reason: Reason for the version change
        edited_by: User who made the change
        edited_at: Timestamp when the change was made
    """
    __tablename__ = 'variable_versions'

    # Primary key with index for faster lookups
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    
    # Foreign key with cascade delete - when variable is deleted, versions are deleted
    variable_id: Mapped[int] = Column(Integer, ForeignKey('variables.id', ondelete='CASCADE'), nullable=False)
    
    # Version number for tracking changes
    version: Mapped[str] = Column(String(50), nullable=False)
    
    # The actual SQL script that performs the calculation
    code: Mapped[str] = Column(Text, nullable=False)
    
    # Optional fields for tracking changes and auditing
    change_reason: Optional[str] = Column(Text)
    created_by: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = Column(Boolean, default=True)
    additional_metadata: Mapped[Optional[dict]] = Column(JSON, nullable=True)

    # Relationships
    # Back-reference to parent variable
    variable: Mapped["Variable"] = relationship('Variable', back_populates='versions')
    
    # Relationship to executions with cascade delete
    executions: Mapped[List['VariableExecution']] = relationship(
        'VariableExecution', 
        back_populates='version',
        cascade="all, delete-orphan"  # Delete executions when version is deleted
    )

    # Ensure unique version numbers per variable
    __table_args__ = (
        UniqueConstraint('variable_id', 'version', name='uix_variable_version'),
    )


class VariableResult(Base):
    """
    Represents the result of a variable calculation.
    
    This model stores the results of variable calculations for specific applications.
    Each result is linked to both the variable and the application.
    
    Attributes:
        id: Unique identifier
        application_id: ID of the application
        variable_id: ID of the calculated variable
        value: Calculated value
        calculated_by: System or user who calculated the value
        calculated_at: Timestamp when the calculation was performed
    """
    __tablename__ = 'variable_results'

    # Primary key with index for faster lookups
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    
    # Application identifier - links to the application being scored
    application_id: str = Column(String(50), nullable=False)
    
    # Foreign key with cascade delete - when variable is deleted, results are deleted
    variable_id: Mapped[int] = Column(Integer, ForeignKey('variables.id', ondelete='CASCADE'), nullable=False)
    
    # The calculated value stored as JSON for flexibility
    result: Mapped[dict] = Column(JSON, nullable=False)
    
    # Audit fields
    created_by: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    additional_metadata: Mapped[Optional[dict]] = Column(JSON, nullable=True)

    # Relationships
    # Back-reference to parent variable
    variable: Mapped["Variable"] = relationship('Variable', back_populates='results')
    
    # Relationship to executions with cascade delete
    executions: Mapped[List['VariableExecution']] = relationship(
        'VariableExecution', 
        back_populates='result',
        cascade="all, delete-orphan"  # Delete executions when result is deleted
    )

    # Ensure unique results per application and variable
    __table_args__ = (
        UniqueConstraint('application_id', 'variable_id', name='uix_application_variable'),
    )


class VariableExecution(Base):
    """
    Represents the execution log of a variable calculation.
    
    This model tracks the execution history of variable calculations,
    including any errors or issues that occurred during execution.
    
    Attributes:
        id: Unique identifier
        application_id: ID of the application
        variable_id: ID of the calculated variable
        executed_by: System or user who executed the calculation
        result: Result of the execution
        executed_at: Timestamp when the execution was performed
    """
    __tablename__ = 'variable_executions'

    # Primary key with index for faster lookups
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    
    # Application identifier - links to the application being scored
    application_id: str = Column(String(50), nullable=False)
    
    # Optional foreign key (allows NULL for failed executions)
    variable_id: Optional[int] = Column(Integer, ForeignKey('variables.id', ondelete='SET NULL'))
    
    # Audit fields
    executed_by: Mapped[Optional[str]] = Column(String(255), nullable=True)
    result_id: Mapped[int] = Column(Integer, ForeignKey('variable_results.id'), nullable=False)
    executed_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[str] = Column(String(50), nullable=False)
    error_message: Mapped[Optional[str]] = Column(Text, nullable=True)
    additional_metadata: Mapped[Optional[dict]] = Column(JSON, nullable=True)

    # Relationships
    version_id: Mapped[int] = Column(Integer, ForeignKey('variable_versions.id'), nullable=False)
    result: Mapped["VariableResult"] = relationship('VariableResult', back_populates='executions')
    version: Mapped["VariableVersion"] = relationship('VariableVersion', back_populates='executions')
