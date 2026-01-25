"""Suggestions API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import Suggestion, SuggestionStatus, AgentType, SuggestionRepository

router = APIRouter(prefix="/api/suggestions", tags=["suggestions"])


class SuggestionResponse(BaseModel):
    id: int
    agent_type: str
    project_id: int
    code_file_id: Optional[int]
    issue_id: Optional[int]
    content: str
    status: str
    created_at: str
    updated_at: str

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            self.updated_at = self.updated_at.isoformat()
        return self

    class Config:
        from_attributes = True


@router.get("/", response_model=List[SuggestionResponse])
def list_suggestions(
    project_id: Optional[int] = None,
    agent_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all suggestions with optional filters."""
    query = db.query(Suggestion)

    if project_id:
        query = query.filter(Suggestion.project_id == project_id)
    if agent_type:
        try:
            agent_enum = AgentType(agent_type)
            query = query.filter(Suggestion.agent_type == agent_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid agent type")
    if status:
        try:
            status_enum = SuggestionStatus(status)
            query = query.filter(Suggestion.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")

    suggestions = query.order_by(Suggestion.created_at.desc()).all()
    # Convert datetime fields to strings
    result = []
    for suggestion in suggestions:
        suggestion_dict = {
            "id": suggestion.id,
            "agent_type": suggestion.agent_type.value,
            "project_id": suggestion.project_id,
            "code_file_id": suggestion.code_file_id,
            "issue_id": suggestion.issue_id,
            "content": suggestion.content,
            "status": suggestion.status.value,
            "created_at": suggestion.created_at.isoformat() if suggestion.created_at else "",
            "updated_at": suggestion.updated_at.isoformat() if suggestion.updated_at else ""
        }
        result.append(SuggestionResponse(**suggestion_dict))
    return result


@router.get("/{suggestion_id}", response_model=SuggestionResponse)
def get_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    """Get suggestion by ID."""
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    suggestion_dict = {
        "id": suggestion.id,
        "agent_type": suggestion.agent_type.value,
        "project_id": suggestion.project_id,
        "code_file_id": suggestion.code_file_id,
        "issue_id": suggestion.issue_id,
        "content": suggestion.content,
        "status": suggestion.status.value,
        "created_at": suggestion.created_at.isoformat() if suggestion.created_at else "",
        "updated_at": suggestion.updated_at.isoformat() if suggestion.updated_at else ""
    }
    return SuggestionResponse(**suggestion_dict)
