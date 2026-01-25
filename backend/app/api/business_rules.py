"""Business Rules API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import BusinessRule, RuleVersion, RuleStatus, BusinessRuleRepository, RuleVersionRepository
from ..services.rule_service import RuleService

router = APIRouter(prefix="/api/business-rules", tags=["business-rules"])


class BusinessRuleCreate(BaseModel):
    content: str
    assumptions: Optional[str] = None
    created_by: Optional[str] = "system"


class BusinessRuleUpdate(BaseModel):
    content: Optional[str] = None
    assumptions: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = "system"


class BusinessRuleResponse(BaseModel):
    id: int
    rule_id: str
    project_id: int
    version: str
    content: str
    status: str
    assumptions: Optional[str]
    created_by: Optional[str]
    approved_by: Optional[str]
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


class RuleVersionResponse(BaseModel):
    id: int
    rule_id: str
    version: str
    content: str
    diff: Optional[str]
    created_at: str
    created_by: Optional[str]

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.isoformat()
        return self

    class Config:
        from_attributes = True


@router.post("/projects/{project_id}/rules", response_model=BusinessRuleResponse)
def create_business_rule(
    project_id: int,
    rule: BusinessRuleCreate,
    db: Session = Depends(get_db)
):
    """Create a new business rule."""
    from ..tables import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    rule_id = RuleService.generate_rule_id(db, project_id)
    
    business_rule = BusinessRule(
        rule_id=rule_id,
        project_id=project_id,
        version="1.0.0",
        content=rule.content,
        status=RuleStatus.DRAFT,
        assumptions=rule.assumptions,
        created_by=rule.created_by
    )
    db.add(business_rule)
    db.commit()
    db.refresh(business_rule)

    rule_dict = {
        "id": business_rule.id,
        "rule_id": business_rule.rule_id,
        "project_id": business_rule.project_id,
        "version": business_rule.version,
        "content": business_rule.content,
        "status": business_rule.status.value,
        "assumptions": business_rule.assumptions,
        "created_by": business_rule.created_by,
        "approved_by": business_rule.approved_by,
        "created_at": business_rule.created_at.isoformat() if business_rule.created_at else "",
        "updated_at": business_rule.updated_at.isoformat() if business_rule.updated_at else ""
    }
    return BusinessRuleResponse(**rule_dict)


@router.get("/projects/{project_id}/rules", response_model=List[BusinessRuleResponse])
def list_business_rules(
    project_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all business rules for a project."""
    query = db.query(BusinessRule).filter(BusinessRule.project_id == project_id)
    
    if status:
        try:
            status_enum = RuleStatus(status)
            query = query.filter(BusinessRule.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")

    rules = query.order_by(BusinessRule.created_at.desc()).all()
    result = []
    for rule in rules:
        rule_dict = {
            "id": rule.id,
            "rule_id": rule.rule_id,
            "project_id": rule.project_id,
            "version": rule.version,
            "content": rule.content,
            "status": rule.status.value,
            "assumptions": rule.assumptions,
            "created_by": rule.created_by,
            "approved_by": rule.approved_by,
            "created_at": rule.created_at.isoformat() if rule.created_at else "",
            "updated_at": rule.updated_at.isoformat() if rule.updated_at else ""
        }
        result.append(BusinessRuleResponse(**rule_dict))
    return result


@router.get("/rules/{rule_id}", response_model=BusinessRuleResponse)
def get_business_rule(rule_id: str, db: Session = Depends(get_db)):
    """Get business rule by Rule ID."""
    rule = RuleService.get_rule_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Business rule not found")
    
    rule_dict = {
        "id": rule.id,
        "rule_id": rule.rule_id,
        "project_id": rule.project_id,
        "version": rule.version,
        "content": rule.content,
        "status": rule.status.value,
        "assumptions": rule.assumptions,
        "created_by": rule.created_by,
        "approved_by": rule.approved_by,
        "created_at": rule.created_at.isoformat() if rule.created_at else "",
        "updated_at": rule.updated_at.isoformat() if rule.updated_at else ""
    }
    return BusinessRuleResponse(**rule_dict)


@router.put("/rules/{rule_id}", response_model=BusinessRuleResponse)
def update_business_rule(
    rule_id: str,
    rule_update: BusinessRuleUpdate,
    db: Session = Depends(get_db)
):
    """Update a business rule (creates new version)."""
    rule = RuleService.get_rule_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Business rule not found")

    # Create new version
    RuleService.create_rule_version(
        db=db,
        rule=rule,
        new_content=rule_update.content,
        created_by=rule_update.created_by or "system"
    )

    # Update rule
    if rule_update.content:
        rule.content = rule_update.content
    if rule_update.assumptions:
        rule.assumptions = rule_update.assumptions
    if rule_update.status:
        try:
            rule.status = RuleStatus(rule_update.status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {rule_update.status}")
    else:
        # Only set to pending_approval if content was updated
        if rule_update.content:
            rule.status = RuleStatus.PENDING_APPROVAL
    db.commit()
    db.refresh(rule)

    rule_dict = {
        "id": rule.id,
        "rule_id": rule.rule_id,
        "project_id": rule.project_id,
        "version": rule.version,
        "content": rule.content,
        "status": rule.status.value,
        "assumptions": rule.assumptions,
        "created_by": rule.created_by,
        "approved_by": rule.approved_by,
        "created_at": rule.created_at.isoformat() if rule.created_at else "",
        "updated_at": rule.updated_at.isoformat() if rule.updated_at else ""
    }
    return BusinessRuleResponse(**rule_dict)


class ApproveRequest(BaseModel):
    approved_by: str


@router.post("/rules/{rule_id}/approve", response_model=BusinessRuleResponse)
def approve_business_rule(
    rule_id: str,
    request: ApproveRequest,
    db: Session = Depends(get_db)
):
    """Approve a business rule."""
    rule = RuleService.get_rule_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Business rule not found")

    rule.status = RuleStatus.APPROVED
    rule.approved_by = request.approved_by
    db.commit()
    db.refresh(rule)

    rule_dict = {
        "id": rule.id,
        "rule_id": rule.rule_id,
        "project_id": rule.project_id,
        "version": rule.version,
        "content": rule.content,
        "status": rule.status.value,
        "assumptions": rule.assumptions,
        "created_by": rule.created_by,
        "approved_by": rule.approved_by,
        "created_at": rule.created_at.isoformat() if rule.created_at else "",
        "updated_at": rule.updated_at.isoformat() if rule.updated_at else ""
    }
    return BusinessRuleResponse(**rule_dict)


@router.get("/rules/{rule_id}/versions", response_model=List[RuleVersionResponse])
def get_rule_versions(rule_id: str, db: Session = Depends(get_db)):
    """Get version history for a business rule."""
    versions = RuleService.get_rule_versions(db, rule_id)
    result = []
    for version in versions:
        version_dict = {
            "id": version.id,
            "rule_id": version.rule_id,
            "version": version.version,
            "content": version.content,
            "diff": version.diff,
            "created_at": version.created_at.isoformat() if version.created_at else "",
            "created_by": version.created_by
        }
        result.append(RuleVersionResponse(**version_dict))
    return result
