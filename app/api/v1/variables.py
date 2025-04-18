from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.variables import Variables
from app.schemas.variables import VariableCreate, VariableResponse

router = APIRouter()

# Create a new variable
@router.post("/variables/", response_model=VariableResponse)
def create_variable(variable: VariableCreate, db: Session = Depends(get_db)):
    db_variable = Variables(**variable.dict())
    db.add(db_variable)
    db.commit()
    db.refresh(db_variable)
    return db_variable




# Fetch all variables or a specific one by ID
@router.get("/variables/", response_model=List[VariableResponse])
def get_variables(
    variable_id: Optional[List[int]] = Query(None, description="List of variable IDs to fetch"),
    db: Session = Depends(get_db)
):
    query = db.query(Variables)
    if variable_id:
        query = query.filter(Variables.id.in_(variable_id))  # Filter for matching IDs

    variables = query.all()
    if not variables:
        raise HTTPException(status_code=404, detail="No variables found matching the given IDs")

    return variables




# Update a specific variable
@router.put("/variables/", response_model=VariableResponse)
def update_variable(
    variable_id: int = Query(..., description="The ID of the variable to update"),
    updated_data: VariableCreate = ...,
    db: Session = Depends(get_db)
):
    db_variable = db.query(Variables).filter(Variables.id == variable_id).first()
    if not db_variable:
        raise HTTPException(status_code=404, detail=f"Variable with ID {variable_id} not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_variable, key, value)

    db.commit()
    db.refresh(db_variable)
    return db_variable




# Delete a specific variable
@router.delete("/variables/", response_model=dict)
def delete_variable(
    variable_id: int = Query(..., description="The ID of the variable to delete"),
    db: Session = Depends(get_db)
):
    db_variable = db.query(Variables).filter(Variables.id == variable_id).first()
    if not db_variable:
        raise HTTPException(status_code=404, detail=f"Variable with ID {variable_id} not found")

    db.delete(db_variable)
    db.commit()
    return {"detail": f"Variable with ID {variable_id} deleted successfully"}
