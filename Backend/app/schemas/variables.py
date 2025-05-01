"""
Pydantic schemas for the Credit Scoring Engine API.
This module defines the data validation schemas for variable operations and responses.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enum defining the possible calculation types for variables
# This ensures type safety and validation of calculation types
class CalculationType(str, Enum):
    """
    Enumeration of possible calculation types for variables.
    
    This enum ensures that only valid calculation types can be used when creating or updating variables.
    The values are used to determine how the variable's SQL script should be executed.
    """
    LIVE = "live"    # Real-time calculation using live database
    DWH = "dwh"      # Data warehouse calculation using historical data
    HYBRID = "hybrid"  # Combination of live and DWH calculations


# Base schema containing common fields for all variable-related schemas
# This follows DRY principle and ensures consistency across variable operations
class VariableBase(BaseModel):
    """
    Base schema for variable operations.
    
    This schema contains the common fields shared across all variable-related operations.
    It serves as the foundation for create, update, and response schemas.
    """
    # Name must be between 1 and 100 characters and must be unique
    name: str = Field(..., min_length=1, max_length=100, description="Unique name of the variable")
    # Optional description with max length of 500 characters
    description: Optional[str] = Field(None, max_length=500, description="Description of the variable's purpose")
    # Calculation type must be one of the defined enum values
    calculation_type: CalculationType = Field(..., description="Type of calculation (live/dwh/hybrid)")


# Schema for creating a new variable
# Inherits from VariableBase to reuse common fields
class VariableCreate(VariableBase):
    """
    Schema for creating a new variable.
    
    This schema defines the required fields when creating a new variable.
    It extends VariableBase to include the SQL script and creator information.
    """
    # SQL script is required and must not be empty
    sql_script: str = Field(..., min_length=1, description="SQL script for variable calculation")
    # Creator's name must be between 1 and 50 characters
    created_by: str = Field(..., min_length=1, max_length=50, description="User creating the variable")


# Schema for updating an existing variable
# Separate from create as it has different required fields
class VariableUpdate(BaseModel):
    """
    Schema for updating a variable.
    
    This schema defines the required fields when updating an existing variable.
    It requires a new SQL script, change reason, and editor information.
    """
    # New SQL script is required and must not be empty
    sql_script: str = Field(..., min_length=1, description="New SQL script for variable calculation")
    # Reason for update must be between 1 and 500 characters
    change_reason: str = Field(..., min_length=1, max_length=500, description="Reason for the update")
    # Editor's name must be between 1 and 50 characters
    edited_by: str = Field(..., min_length=1, max_length=50, description="User making the update")


# Schema for variable response
# Inherits from VariableBase and adds response-specific fields
class VariableResponse(VariableBase):
    """
    Schema for variable response.
    
    This schema defines the structure of the response when retrieving a variable.
    It includes additional fields like ID, active status, and creation metadata.
    """
    # Required fields for response
    id: int = Field(..., description="Unique identifier of the variable")
    is_active: bool = Field(..., description="Whether the variable is active")
    created_by: Optional[str] = Field(None, max_length=50, description="User who created the variable")
    created_at: datetime = Field(..., description="Timestamp when the variable was created")

    # Configuration to allow ORM model conversion
    model_config = ConfigDict(from_attributes=True)


# Schema for variable calculation result
class VariableResultResponse(BaseModel):
    """
    Schema for variable calculation result.
    
    This schema defines the structure of the response when retrieving a variable's calculation result.
    It includes the application ID, variable ID, calculated value, and metadata.
    """
    # Required fields for calculation result
    application_id: str = Field(..., min_length=1, max_length=50, description="ID of the application")
    variable_id: int = Field(..., description="ID of the calculated variable")
    value: str = Field(..., description="Calculated value of the variable")
    calculated_by: Optional[str] = Field(None, max_length=50, description="System or user who calculated the value")
    calculated_at: datetime = Field(..., description="Timestamp when the calculation was performed")

    # Configuration to allow ORM model conversion
    model_config = ConfigDict(from_attributes=True)


# Schema for variable calculation request
class VariableCalcRequest(BaseModel):
    """
    Schema for variable calculation request.
    
    This schema defines the structure of the request when calculating variables for an application.
    It requires an application ID and a list of variable IDs to calculate.
    """
    # Application ID must be between 1 and 50 characters
    app_id: str = Field(..., min_length=1, max_length=50, description="ID of the application to calculate variables for")
    # Must provide at least one variable ID to calculate
    variable_ids: List[int] = Field(..., min_items=1, description="List of variable IDs to calculate")


# Schema for error responses
# Used across all endpoints for consistent error handling
class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    This schema defines the structure of error responses returned by the API.
    It includes an error message and HTTP status code.
    """
    detail: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
