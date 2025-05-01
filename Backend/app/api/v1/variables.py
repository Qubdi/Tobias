from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List
from datetime import datetime, timezone
from db import get_db
from models import Variable, VariableVersion
from schemas import (VariableCreate,VariableUpdate,VariableResponse,VariableCalcRequest,ErrorResponse,CalculationType)



# Initialize the router with common configurations
router = APIRouter(
    prefix="/api/variables",  # Base path for all routes in this router
    tags=["Variables"],  # API documentation tag
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Variable not found"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid request"},
    }
)




@router.post("/", response_model=VariableResponse, status_code=status.HTTP_201_CREATED, responses={
        status.HTTP_201_CREATED: {"description": "Variable created successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Variable already exists"},
    })
async def create_variable(payload: VariableCreate, db: Session = Depends(get_db)):
    """
    Create a new credit scoring variable.
    
    This endpoint creates a new variable with its initial version.
    The variable name must be unique, and the SQL script must be valid.
    
    Args:
        payload (VariableCreate): The variable creation payload containing:
            - name: Unique name of the variable
            - description: Description of what the variable calculates
            - calculation_type: Type of calculation (live/dwh/hybrid)
            - sql_script: SQL script for variable calculation
            - created_by: User creating the variable
        db (Session): Database session
    
    Returns:
        VariableResponse: The created variable with its metadata
    
    Raises:
        HTTPException: If a variable with the same name already exists
    """
    # Check if variable with the same name already exists
    if db.query(Variable).filter_by(name=payload.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Variable with this name already exists"
        )


    # Create the Variable object
    var = Variable(
        name=payload.name,
        description=payload.description,
        calculation_type=payload.calculation_type.value,  # Use the enum value
        created_by=payload.created_by,
        created_at=datetime.now(timezone.utc)
    )
    db.add(var)
    db.flush()

    # Add the first version of the variable's SQL
    version = VariableVersion(
        variable_id=var.id,
        version=1,
        code=payload.sql_script,
        created_by=payload.created_by,
        created_at=datetime.now(timezone.utc)
    )
    db.add(version)
    db.commit()
    db.refresh(var)
    return var



@router.get("/", response_model=List[VariableResponse], responses={
        status.HTTP_200_OK: {"description": "List of active variables retrieved successfully"}
    })
async def get_all_variables(db: Session = Depends(get_db)):
    """
    Get all active credit scoring variables.
    
    This endpoint retrieves a list of all active variables in the system.
    Only variables with is_active=True are returned.
    
    Args:
        db (Session): Database session
    
    Returns:
        List[VariableResponse]: List of active variables
    """
    return db.query(Variable).filter_by(is_active=True).all()



@router.get("/{variable_id}", response_model=VariableResponse, responses={
        status.HTTP_200_OK: {"description": "Variable retrieved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Variable not found"}
    })
async def get_variable(variable_id: int, db: Session = Depends(get_db)):
    """
    Get a specific credit scoring variable by ID.
    
    This endpoint retrieves a single variable by its ID.
    The variable must exist and be active.
    
    Args:
        variable_id (int): The ID of the variable to retrieve
        db (Session): Database session
    
    Returns:
        VariableResponse: The requested variable
    
    Raises:
        HTTPException: If the variable is not found or is inactive
    """
    var = db.query(Variable).filter_by(id=variable_id).first()
    if not var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variable not found"
        )
    return var



@router.put("/{variable_id}", response_model=VariableResponse, responses={
        status.HTTP_200_OK: {"description": "Variable updated successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Variable not found"}
    })
async def update_variable(variable_id: int,payload: VariableUpdate,db: Session = Depends(get_db)):
    """
    Update a credit scoring variable.
    
    This endpoint updates an existing variable by creating a new version
    with the updated SQL script. The change reason and editor are recorded.
    
    Args:
        variable_id (int): The ID of the variable to update
        payload (VariableUpdate): The update payload containing:
            - sql_script: New SQL script for the variable
            - change_reason: Reason for the update
            - edited_by: User making the update
        db (Session): Database session
    
    Returns:
        VariableResponse: The updated variable
    
    Raises:
        HTTPException: If the variable is not found or is inactive
    """
    var = db.query(Variable).filter_by(id=variable_id, is_active=True).first()
    if not var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variable not found"
        )

    latest = (
        db.query(VariableVersion)
        .filter_by(variable_id=var.id)
        .order_by(VariableVersion.version_number.desc())
        .first()
    )

    new_version = VariableVersion(
        variable_id=var.id,
        version_number=latest.version_number + 1,
        sql_script=payload.sql_script,
        change_reason=payload.change_reason,
        edited_by=payload.edited_by,
        edited_at=datetime.utcnow()
    )
    db.add(new_version)
    db.commit()
    return var



@router.delete("/{variable_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
        status.HTTP_200_OK: {"description": "Variable deleted successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Variable not found"}
    })
async def delete_variable(variable_id: int, db: Session = Depends(get_db)):
    """
    Delete a credit scoring variable.
    
    This endpoint performs a soft delete on the variable by setting is_active=False.
    The variable and its versions are preserved in the database for audit purposes.
    
    Args:
        variable_id (int): The ID of the variable to delete
        db (Session): Database session
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException: If the variable is not found
    """
    var = db.query(Variable).filter_by(id=variable_id).first()
    if not var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variable not found"
        )

    var.is_active = False
    db.commit()
    
    return {
        "status": "success",
        "message": "Variable deleted successfully",
        "variable_id": variable_id
    }



@router.post("/calculate",responses={
        status.HTTP_200_OK: {"description": "Variables calculated successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request"},
        status.HTTP_404_NOT_FOUND: {"description": "No variable versions found"}
    })
async def calculate_variables(payload: VariableCalcRequest,db: Session = Depends(get_db)):
    """
    Calculate variables for an application.
    
    This endpoint calculates the specified variables for a given application.
    It uses the latest active version of each variable's SQL script.
    
    Args:
        payload (VariableCalcRequest): The calculation request containing:
            - app_id: ID of the application to calculate variables for
            - variable_ids: List of variable IDs to calculate
        db (Session): Database session
    
    Returns:
        dict: Calculation results for each variable
    
    Raises:
        HTTPException: If no active variable versions are found
    """
    if not payload.variable_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No variable_ids provided"
        )

    # Get latest versions
    subquery = (
        db.query(
            VariableVersion.variable_id,
            func.max(VariableVersion.version_number).label("max_version")
        )
        .filter(VariableVersion.variable_id.in_(payload.variable_ids))
        .group_by(VariableVersion.variable_id)
        .subquery()
    )

    latest_versions = (
        db.query(VariableVersion)
        .join(
            subquery,
            (VariableVersion.variable_id == subquery.c.variable_id) &
            (VariableVersion.version_number == subquery.c.max_version)
        )
        .all()
    )

    if not latest_versions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No variable versions found"
        )

    # Prepare CTEs
    cte_blocks = []
    result_selects = []
    execution_selects = []

    for var in latest_versions:
        var_id = var.variable_id
        sql_code = var.sql_script.strip().rstrip(";")

        cte_blocks.append(f"""
        var_{var_id} AS (
            SELECT
                :app_id AS application_id,
                {var_id} AS variable_id,
                CAST((
                    {sql_code}
                ) AS TEXT) AS value
        )
        """.strip())

        result_selects.append(f"SELECT *, 'system' AS calculated_by FROM var_{var_id}")
        execution_selects.append(f"""
        SELECT
            :app_id AS application_id,
            {var_id} AS variable_id,
            'system' AS executed_by,
            value AS result
        FROM var_{var_id}
        """.strip())

    cte_sql = ",\n".join(cte_blocks)
    results_sql = "\nUNION ALL\n".join(result_selects)

    # Insert into variable_results
    sql_results = f"""
    WITH
    {cte_sql}
    INSERT INTO variable_results (application_id, variable_id, value, calculated_by)
    {results_sql};
    """

    db.execute(text(sql_results), {"app_id": payload.app_id})
    db.commit()

    return {
        "status": "success",
        "application_id": payload.app_id,
        "calculated_variables": [v.variable_id for v in latest_versions]
    }

