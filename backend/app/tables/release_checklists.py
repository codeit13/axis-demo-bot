"""Release checklists table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
import json
from ..database import Base


class ReleaseChecklist(Base):
    """Release readiness checklist model."""
    __tablename__ = "release_checklists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    release_version = Column(String(50), nullable=False)
    checklist_items = Column(Text, nullable=True)  # JSON array
    rollback_strategy = Column(Text, nullable=True)
    observability_metrics = Column(Text, nullable=True)  # JSON array
    status = Column(String(50), default="draft", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", lazy="select")


class ReleaseChecklistRepository:
    """Repository methods for ReleaseChecklist table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        project_id: int,
        release_version: str,
        checklist_items: Optional[List[dict]] = None,
        rollback_strategy: Optional[str] = None,
        observability_metrics: Optional[List[dict]] = None,
        status: str = "draft"
    ) -> ReleaseChecklist:
        """Create a new release checklist."""
        checklist = ReleaseChecklist(
            project_id=project_id,
            release_version=release_version,
            checklist_items=json.dumps(checklist_items) if checklist_items else None,
            rollback_strategy=rollback_strategy,
            observability_metrics=json.dumps(observability_metrics) if observability_metrics else None,
            status=status
        )
        self.db.add(checklist)
        self.db.commit()
        self.db.refresh(checklist)
        return checklist

    def get_by_id(self, checklist_id: int) -> Optional[ReleaseChecklist]:
        """Get release checklist by ID."""
        return self.db.query(ReleaseChecklist).filter(ReleaseChecklist.id == checklist_id).first()

    def get_by_project(self, project_id: int) -> List[ReleaseChecklist]:
        """Get all release checklists for a project."""
        return self.db.query(ReleaseChecklist).filter(
            ReleaseChecklist.project_id == project_id
        ).order_by(ReleaseChecklist.created_at.desc()).all()

    def get_by_project_and_version(
        self,
        project_id: int,
        release_version: str
    ) -> Optional[ReleaseChecklist]:
        """Get release checklist by project and version."""
        return self.db.query(ReleaseChecklist).filter(
            ReleaseChecklist.project_id == project_id,
            ReleaseChecklist.release_version == release_version
        ).first()

    def get_checklist_items(self, checklist: ReleaseChecklist) -> List[dict]:
        """Parse and return checklist items from JSON."""
        if not checklist.checklist_items:
            return []
        try:
            return json.loads(checklist.checklist_items)
        except:
            return []

    def get_observability_metrics(self, checklist: ReleaseChecklist) -> List[dict]:
        """Parse and return observability metrics from JSON."""
        if not checklist.observability_metrics:
            return []
        try:
            return json.loads(checklist.observability_metrics)
        except:
            return []

    def update_status(self, checklist_id: int, status: str) -> Optional[ReleaseChecklist]:
        """Update release checklist status."""
        checklist = self.get_by_id(checklist_id)
        if not checklist:
            return None
        
        checklist.status = status
        self.db.commit()
        self.db.refresh(checklist)
        return checklist

    def update(self, checklist_id: int, **kwargs) -> Optional[ReleaseChecklist]:
        """Update release checklist fields."""
        checklist = self.get_by_id(checklist_id)
        if not checklist:
            return None
        
        for key, value in kwargs.items():
            if hasattr(checklist, key):
                if key in ['checklist_items', 'observability_metrics'] and isinstance(value, list):
                    setattr(checklist, key, json.dumps(value))
                else:
                    setattr(checklist, key, value)
        
        self.db.commit()
        self.db.refresh(checklist)
        return checklist

    def delete(self, checklist_id: int) -> bool:
        """Delete a release checklist."""
        checklist = self.get_by_id(checklist_id)
        if not checklist:
            return False
        
        self.db.delete(checklist)
        self.db.commit()
        return True
