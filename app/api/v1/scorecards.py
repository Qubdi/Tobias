from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional

from app.db.session import get_db
from app.models.scorecards import ScoreCards
from app.schemas.scorecards import ScoreCardCreate, ScoreCardUpdate, ScoreCardResponse

router = APIRouter()




@router.post("/scorecards/", response_model=List[ScoreCardResponse])
def upload_scorecards(scorecards: List[ScoreCardCreate], db: Session = Depends(get_db)):
    try:
        # Fetch the next ScoreCardId only if it is not provided
        next_scorecard_id = db.query(func.coalesce(func.max(ScoreCards.ScoreCardId), 0)).scalar() + 1

        scorecard_objects = []
        for scorecard in scorecards:
            # Assign next_scorecard_id if ScoreCardId is not provided
            if not scorecard.ScoreCardId:
                scorecard.ScoreCardId = next_scorecard_id

            scorecard_objects.append(ScoreCards(**scorecard.dict()))

        db.add_all(scorecard_objects)  # Add all objects to the session
        db.commit()  # Commit the transaction

        # Refresh objects to fetch auto-generated "id"
        for obj in scorecard_objects:
            db.refresh(obj)

        return scorecard_objects  # Return the inserted records with IDs
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload ScoreCards: {str(e)}")



# 2. Fetch ScoreCards (supports scorecard_id and range_id as query parameters)
@router.get("/scorecards/", response_model=List[ScoreCardResponse])
def get_scorecards(
    scorecard_id: Optional[int] = Query(None, description="Filter by ScoreCardId"),
    range_id: Optional[int] = Query(None, description="Filter by specific range ID"),
    db: Session = Depends(get_db)
):
    query = db.query(ScoreCards)
    if scorecard_id:
        query = query.filter(ScoreCards.ScoreCardId == scorecard_id)
    if range_id:
        query = query.filter(ScoreCards.id == range_id)

    results = query.all()
    return results  # Return an empty list [] if no records are found



# 3. Update a specific range (requires scorecard_id and range_id)
@router.put("/scorecards/", response_model=ScoreCardResponse)
def update_specific_range(
    scorecard_id: int = Query(..., description="ScoreCardId to identify the record"),
    range_id: int = Query(..., description="Specific range ID to update"),
    scorecard: ScoreCardUpdate = None,
    db: Session = Depends(get_db)
):
    db_scorecard = db.query(ScoreCards).filter(
        ScoreCards.ScoreCardId == scorecard_id, ScoreCards.id == range_id
    ).first()
    if not db_scorecard:
        raise HTTPException(status_code=404, detail="Range not found")

    for key, value in scorecard.dict(exclude_unset=True).items():
        setattr(db_scorecard, key, value)

    db.commit()
    db.refresh(db_scorecard)
    return db_scorecard


# 4. Delete ScoreCard(s) or specific range(s) using scorecard_id and optional range_id
@router.delete("/scorecards/", response_model=dict)
def delete_scorecards(
    scorecard_id: int = Query(..., description="ScoreCardId to delete"),
    range_id: Optional[int] = Query(None, description="Specific range ID to delete"),
    db: Session = Depends(get_db)
):
    if range_id:
        # Delete specific range
        db_scorecard = db.query(ScoreCards).filter(
            ScoreCards.ScoreCardId == scorecard_id, ScoreCards.id == range_id
        ).first()
        if not db_scorecard:
            raise HTTPException(status_code=404, detail="Range not found")
        db.delete(db_scorecard)
        db.commit()
        return {"detail": f"Range with ID {range_id} under ScoreCardId {scorecard_id} deleted successfully"}
    else:
        # Delete all ranges for a ScoreCardId
        db_scorecards = db.query(ScoreCards).filter(ScoreCards.ScoreCardId == scorecard_id).all()
        if not db_scorecards:
            raise HTTPException(status_code=404, detail="No ranges found for this ScoreCardId")
        for scorecard in db_scorecards:
            db.delete(scorecard)
        db.commit()
        return {"detail": f"ScoreCard with ID {scorecard_id} deleted successfully"}
