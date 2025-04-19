from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Variable, VariableVersion
from app.schemas import VariableCreate, VariableUpdate, VariableResponse
from datetime import datetime

router = APIRouter(prefix="/variables", tags=["Variables"])



@router.post("/", response_model=VariableResponse)
def create_variable(payload: VariableCreate, db: Session = Depends(get_db)):
    # Check if variable with the same name already exists
    if db.query(Variable).filter_by(name=payload.name).first():
        raise HTTPException(status_code=400, detail="Variable already exists")

    # Create the Variable object
    var = Variable(
        name=payload.name,
        description=payload.description,
        calculation_type=payload.calculation_type,
        created_by=payload.created_by,
    )
    db.add(var)      # Add to session
    db.flush()       # Ensure var.id is available before committing

    # Add the first version of the variable's SQL
    version = VariableVersion(
        variable_id=var.id,
        version_number=1,
        sql_script=payload.sql_script,
        change_reason="Initial version",
        edited_by=payload.created_by,
    )
    db.add(version)  # Add version record
    db.commit()      # Commit both inserts
    db.refresh(var)  # Refresh the variable object to get full state
    return var       # Return the new variable



@router.get("/", response_model=list[VariableResponse])
def get_all_variables(db: Session = Depends(get_db)):
    # Query all variables where is_active is True
    return db.query(Variable).filter_by(is_active=True).all()



@router.get("/{variable_id}", response_model=VariableResponse)
def get_variable(variable_id: int, db: Session = Depends(get_db)):
    # Try to find variable by ID
    var = db.query(Variable).filter_by(id=variable_id).first()
    if not var:
        raise HTTPException(status_code=404, detail="Variable not found")
    return var



@router.put("/{variable_id}", response_model=VariableResponse)
def update_variable(variable_id: int, payload: VariableUpdate, db: Session = Depends(get_db)):
    # Find the active variable
    var = db.query(Variable).filter_by(id=variable_id, is_active=True).first()
    if not var:
        raise HTTPException(status_code=404, detail="Variable not found")

    # Get the latest version number
    latest = (
        db.query(VariableVersion)
        .filter_by(variable_id=var.id)
        .order_by(VariableVersion.version_number.desc())
        .first()
    )

    # Add a new version with incremented version_number
    new_version = VariableVersion(
        variable_id=var.id,
        version_number=latest.version_number + 1,
        sql_script=payload.sql_script,
        change_reason=payload.change_reason,
        edited_by=payload.edited_by,
    )
    db.add(new_version)  # Add to session
    db.commit()          # Commit the update
    return var           # Return the updated variable




@router.delete("/{variable_id}")
def delete_variable(variable_id: int, db: Session = Depends(get_db)):
    # Look up the variable by ID
    var = db.query(Variable).filter_by(id=variable_id).first()
    if not var:
        raise HTTPException(status_code=404, detail="Variable not found")

    # Soft delete: mark as inactive
    var.is_active = False
    db.commit()  # Save change to DB
    return {"message": f"Variable {var.name} marked as inactive"}
