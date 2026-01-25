"""Issues API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import Issue, IssueStatus, IssueRepository
from ..services.bitbucket_mock import BitbucketMockService

router = APIRouter(prefix="/api/issues", tags=["issues"])


class IssueCreate(BaseModel):
    title: str
    description: str
    code_file_id: Optional[int] = None


class IssueResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    status: str
    bitbucket_issue_id: Optional[str]
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


@router.post("/projects/{project_id}/issues", response_model=IssueResponse)
def create_issue(
    project_id: int,
    issue: IssueCreate,
    db: Session = Depends(get_db)
):
    """Create a new issue (with mock Bitbucket integration)."""
    from ..tables import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = BitbucketMockService.create_issue(
        db=db,
        project_id=project_id,
        title=issue.title,
        description=issue.description,
        code_file_id=issue.code_file_id
    )

    db_issue = db.query(Issue).filter(Issue.id == result["id"]).first()
    issue_dict = {
        "id": db_issue.id,
        "project_id": db_issue.project_id,
        "title": db_issue.title,
        "description": db_issue.description,
        "status": db_issue.status.value,
        "bitbucket_issue_id": db_issue.bitbucket_issue_id,
        "created_at": db_issue.created_at.isoformat() if db_issue.created_at else "",
        "updated_at": db_issue.updated_at.isoformat() if db_issue.updated_at else ""
    }
    return IssueResponse(**issue_dict)


@router.get("/projects/{project_id}/issues", response_model=List[IssueResponse])
def list_issues(project_id: int, db: Session = Depends(get_db)):
    """List all issues for a project."""
    issues = db.query(Issue).filter(Issue.project_id == project_id).all()
    result = []
    for issue in issues:
        issue_dict = {
            "id": issue.id,
            "project_id": issue.project_id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status.value,
            "bitbucket_issue_id": issue.bitbucket_issue_id,
            "created_at": issue.created_at.isoformat() if issue.created_at else "",
            "updated_at": issue.updated_at.isoformat() if issue.updated_at else ""
        }
        result.append(IssueResponse(**issue_dict))
    return result


@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get issue by ID."""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue_dict = {
        "id": issue.id,
        "project_id": issue.project_id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status.value,
        "bitbucket_issue_id": issue.bitbucket_issue_id,
        "created_at": issue.created_at.isoformat() if issue.created_at else "",
        "updated_at": issue.updated_at.isoformat() if issue.updated_at else ""
    }
    return IssueResponse(**issue_dict)


@router.patch("/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update issue status."""
    try:
        status_enum = IssueStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = BitbucketMockService.update_issue_status(db, issue_id, status_enum)
    if not result:
        raise HTTPException(status_code=404, detail="Issue not found")
    return result
