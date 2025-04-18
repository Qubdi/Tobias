from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.rules import Rules
from app.schemas.rules import RuleCreate, RuleUpdate, RuleResponse
from typing import List, Optional
from fastapi import Query


router = APIRouter()

# Add a new rule
@router.post("/rules/")
def create_rule(rule_data: dict, db: Session = Depends(get_db)):
    try:
        rule = Rules(**rule_data)
        # rule = Rules(
        #     RuleName=str(rule_data["RuleName"]),
        #     VariableId=int(rule_data["VariableId"]),
        #     Allowed=str(rule_data.get("Allowed", "")),
        #     NotAllowed=str(rule_data.get("NotAllowed", "")),
        #     StartRange=float(rule_data.get("StartRange", "")),  # Convert to string
        #     EndRange=float(rule_data.get("EndRange", "")),      # Convert to string
        #     RuleValue=str(rule_data.get("RuleValue", "")),
        #     RuleType=str(rule_data.get("RuleType", ""))
        # )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# Fetch rules by id(s) or return all
@router.get("/rules/", response_model=List[RuleResponse])
# Optional query parameter for multiple IDs
def get_rules(rule_id: Optional[List[int]] = Query(None), db: Session = Depends(get_db)):
    if rule_id:  # If specific rule_ids are provided
        rules = db.query(Rules).filter(Rules.id.in_(rule_id)).all()
        if not rules:
            raise HTTPException(status_code=404, detail="No rules found for the given IDs.")
        return rules
    else:  # If no rule_ids are provided, fetch all
        return db.query(Rules).all()




# Update a specific rule
@router.put("/rules/", response_model=RuleResponse)
# Optional but validated manually
def update_rule(
    rule_id: Optional[int] = Query(None, description="The ID of the rule to update"),
    updated_data: dict = {},
    db: Session = Depends(get_db)
):
    if not rule_id:
        raise HTTPException(status_code=400, detail="rule_id query parameter is required.")

    rule = db.query(Rules).filter(Rules.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule with ID {rule_id} not found")

    # Update logic
    for key, value in updated_data.items():
        if hasattr(rule, key) and value is not None:
            setattr(rule, key, value)

    db.commit()
    db.refresh(rule)
    return rule


# Delete a specific rule
@router.delete("/rules/", response_model=dict)
def delete_rule(
    rule_id: Optional[int] = Query(None, description="The ID of the rule to delete"),  # Optional but validated manually
    db: Session = Depends(get_db)
):
    if not rule_id:
        raise HTTPException(status_code=400, detail="rule_id query parameter is required.")

    rule = db.query(Rules).filter(Rules.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule with ID {rule_id} not found")

    db.delete(rule)
    db.commit()
    return {"detail": f"Rule with ID {rule_id} deleted successfully"}