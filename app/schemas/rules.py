from pydantic import BaseModel
from typing import Optional

# Schema for reading and creating rules
class RuleBase(BaseModel):
    RuleName: str
    VariableId: int
    Allowed: Optional[str] = None
    NotAllowed: Optional[str] = None
    StartRange: Optional[float] = None
    EndRange: Optional[float] = None
    RuleValue: Optional[str] = None
    RuleType: Optional[str] = None

class RuleCreate(RuleBase):
    pass

class RuleUpdate(RuleBase):
    pass

class RuleResponse(RuleBase):
    id: int

    class Config:
        orm_mode = True
