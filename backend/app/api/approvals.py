"""Approvals API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import Approval, Suggestion, SuggestionStatus, ApprovalRepository

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


class ApprovalRequest(BaseModel):
    user_action: str  # "approve", "reject", "modify"
    comments: Optional[str] = ""


class ApprovalResponse(BaseModel):
    id: int
    suggestion_id: int
    user_action: str
    comments: Optional[str]
    timestamp: str

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.timestamp, datetime):
            self.timestamp = self.timestamp.isoformat()
        return self

    class Config:
        from_attributes = True


@router.post("/suggestions/{suggestion_id}/approve", response_model=ApprovalResponse)
def approve_suggestion(
    suggestion_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db)
):
    """Approve or reject a suggestion."""
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    if request.user_action == "approve":
        suggestion.status = SuggestionStatus.APPROVED
    elif request.user_action == "reject":
        suggestion.status = SuggestionStatus.REJECTED
    elif request.user_action == "modify":
        # Keep as pending for modification
        suggestion.status = SuggestionStatus.PENDING
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'approve', 'reject', or 'modify'")

    # Create approval record
    approval = Approval(
        suggestion_id=suggestion_id,
        user_action=request.user_action,
        comments=request.comments
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)

    approval_dict = {
        "id": approval.id,
        "suggestion_id": approval.suggestion_id,
        "user_action": approval.user_action,
        "comments": approval.comments,
        "timestamp": approval.timestamp.isoformat() if approval.timestamp else ""
    }
    return ApprovalResponse(**approval_dict)


@router.get("/suggestions/{suggestion_id}/history", response_model=list[ApprovalResponse])
def get_approval_history(suggestion_id: int, db: Session = Depends(get_db)):
    """Get approval history for a suggestion."""
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    approvals = db.query(Approval).filter(Approval.suggestion_id == suggestion_id).all()
    result = []
    for approval in approvals:
        approval_dict = {
            "id": approval.id,
            "suggestion_id": approval.suggestion_id,
            "user_action": approval.user_action,
            "comments": approval.comments,
            "timestamp": approval.timestamp.isoformat() if approval.timestamp else ""
        }
        result.append(ApprovalResponse(**approval_dict))
    return result
