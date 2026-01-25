"""Issues table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
import enum
from ..database import Base


class IssueStatus(str, enum.Enum):
    """Issue status enumeration."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Issue(Base):
    """Issue/Bug model."""
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(IssueStatus), default=IssueStatus.OPEN, nullable=False, index=True)
    bitbucket_issue_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="issues", lazy="select")
    suggestions = relationship("Suggestion", back_populates="issue", lazy="select")


class IssueRepository:
    """Repository methods for Issue table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        bitbucket_issue_id: Optional[str] = None
    ) -> Issue:
        """Create a new issue."""
        issue = Issue(
            project_id=project_id,
            title=title,
            description=description,
            bitbucket_issue_id=bitbucket_issue_id
        )
        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        """Get issue by ID."""
        return self.db.query(Issue).filter(Issue.id == issue_id).first()

    def get_by_project(self, project_id: int, status: Optional[IssueStatus] = None) -> List[Issue]:
        """Get all issues for a project, optionally filtered by status."""
        query = self.db.query(Issue).filter(Issue.project_id == project_id)
        if status:
            query = query.filter(Issue.status == status)
        return query.order_by(Issue.created_at.desc()).all()

    def update_status(self, issue_id: int, status: IssueStatus) -> Optional[Issue]:
        """Update issue status."""
        issue = self.get_by_id(issue_id)
        if not issue:
            return None
        
        issue.status = status
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def update(self, issue_id: int, **kwargs) -> Optional[Issue]:
        """Update issue fields."""
        issue = self.get_by_id(issue_id)
        if not issue:
            return None
        
        for key, value in kwargs.items():
            if hasattr(issue, key):
                setattr(issue, key, value)
        
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def delete(self, issue_id: int) -> bool:
        """Delete an issue."""
        issue = self.get_by_id(issue_id)
        if not issue:
            return False
        
        self.db.delete(issue)
        self.db.commit()
        return True
