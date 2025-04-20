from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VariableCreate(BaseModel):
    name: str
    description: Optional[str]
    calculation_type: str
    created_by: str
    sql_script: str


class VariableUpdate(BaseModel):
    sql_script: str
    change_reason: str
    edited_by: str


class VariableResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    calculation_type: str
    is_active: bool
    created_by: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class VariableResultResponse(BaseModel):
    application_id: str
    variable_id: int
    value: str
    calculated_by: Optional[str]
    calculated_at: datetime

    model_config = {
        "from_attributes": True
    }
