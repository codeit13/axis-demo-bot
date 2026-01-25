"""Change Impact API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import ChangeImpact, ChangeType, RiskLevel, ChangeImpactRepository

router = APIRouter(prefix="/api/change-impact", tags=["change-impact"])


class ChangeImpactResponse(BaseModel):
    id: int
    project_id: int
    change_type: str
    affected_rule_ids: str  # JSON array
    affected_agents: str  # JSON array
    required_reruns: str  # JSON array
    risk_level: str
    analysis_result: str  # JSON
    created_at: str

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.isoformat()
        return self

    class Config:
        from_attributes = True


class ChangeImpactRequest(BaseModel):
    project_id: int
    change_type: str
    rule_ids: Optional[List[str]] = None


@router.post("/analyze")
async def analyze_change_impact(
    request: ChangeImpactRequest,
    db: Session = Depends(get_db)
):
    """Run change impact analysis."""
    from ..agents.change_impact_agent import ChangeImpactAgent
    
    try:
        agent = ChangeImpactAgent(db)
        result = agent.analyze(
            project_id=request.project_id,
            change_type=request.change_type,
            rule_ids=request.rule_ids or []
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/impacts", response_model=List[ChangeImpactResponse])
def list_change_impacts(project_id: int, db: Session = Depends(get_db)):
    """List all change impacts for a project."""
    impacts = db.query(ChangeImpact).filter(
        ChangeImpact.project_id == project_id
    ).order_by(ChangeImpact.created_at.desc()).all()
    
    result = []
    for impact in impacts:
        impact_dict = {
            "id": impact.id,
            "project_id": impact.project_id,
            "change_type": impact.change_type.value,
            "affected_rule_ids": impact.affected_rule_ids,
            "affected_agents": impact.affected_agents,
            "required_reruns": impact.required_reruns,
            "risk_level": impact.risk_level.value,
            "analysis_result": impact.analysis_result,
            "created_at": impact.created_at.isoformat() if impact.created_at else ""
        }
        result.append(ChangeImpactResponse(**impact_dict))
    return result


@router.get("/{impact_id}", response_model=ChangeImpactResponse)
def get_change_impact(impact_id: int, db: Session = Depends(get_db)):
    """Get change impact by ID."""
    impact = db.query(ChangeImpact).filter(ChangeImpact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail="Change impact not found")
    
    impact_dict = {
        "id": impact.id,
        "project_id": impact.project_id,
        "change_type": impact.change_type.value,
        "affected_rule_ids": impact.affected_rule_ids,
        "affected_agents": impact.affected_agents,
        "required_reruns": impact.required_reruns,
        "risk_level": impact.risk_level.value,
        "analysis_result": impact.analysis_result,
        "created_at": impact.created_at.isoformat() if impact.created_at else ""
    }
    return ChangeImpactResponse(**impact_dict)
