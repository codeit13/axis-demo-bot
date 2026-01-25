"""Projects table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
from ..database import Base


class Project(Base):
    """Project model."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    repository_url = Column(String(512), nullable=True)
    business_logic_version = Column(String(50), default="1.0.0", nullable=False)
    current_rule_set_id = Column(Integer, ForeignKey("business_rules.id"), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships (lazy loading)
    code_files = relationship("CodeFile", back_populates="project", cascade="all, delete-orphan", lazy="select")
    issues = relationship("Issue", back_populates="project", cascade="all, delete-orphan", lazy="select")
    suggestions = relationship("Suggestion", back_populates="project", cascade="all, delete-orphan", lazy="select")
    business_rules = relationship(
        "BusinessRule",
        back_populates="project",
        foreign_keys="BusinessRule.project_id",
        cascade="all, delete-orphan",
        lazy="select"
    )
    current_rule_set = relationship("BusinessRule", foreign_keys=[current_rule_set_id], uselist=False, lazy="select")


class ProjectRepository:
    """Repository methods for Project table."""

    def __init__(self, db):
        self.db = db

    def create(self, name: str, description: Optional[str] = None, repository_url: Optional[str] = None) -> Project:
        """Create a new project."""
        project = Project(
            name=name,
            description=description,
            repository_url=repository_url
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_all(self) -> List[Project]:
        """Get all projects."""
        return self.db.query(Project).order_by(Project.created_at.desc()).all()

    def update(self, project_id: int, **kwargs) -> Optional[Project]:
        """Update project fields."""
        project = self.get_by_id(project_id)
        if not project:
            return None
        
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        """Delete a project."""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        self.db.delete(project)
        self.db.commit()
        return True

    def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name."""
        return self.db.query(Project).filter(Project.name == name).first()
