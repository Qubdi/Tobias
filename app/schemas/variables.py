from pydantic import BaseModel
from typing import Optional

# Request model for creating/updating a variable
class VariableCreate(BaseModel):
    VariableName: str
    Logic: Optional[str] = None
    VariableType: Optional[str] = None
    DBType: Optional[str] = None

# Response model for retrieving variables
class VariableResponse(VariableCreate):
    id: int  # Primary key

    class Config:
        orm_mode = True  # Allows ORM to work with Pydantic models