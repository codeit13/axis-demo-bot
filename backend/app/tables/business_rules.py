"""Business rules table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func
from typing import Optional, List
import enum
from ..database import Base


class RuleStatus(str, enum.Enum):
    """Business rule status enumeration."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DEPRECATED = "deprecated"


class BusinessRule(Base):
    """Business Logic & Policy Rule model."""
    __tablename__ = "business_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_id = Column(String(50), nullable=False, unique=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(50), nullable=False, default="1.0.0")
    content = Column(Text, nullable=False)
    status = Column(SQLEnum(RuleStatus), default=RuleStatus.DRAFT, nullable=False, index=True)
    assumptions = Column(Text, nullable=True)
    created_by = Column(String(255), nullable=True)
    approved_by = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="business_rules", foreign_keys=[project_id], lazy="select")
    versions = relationship("RuleVersion", back_populates="rule", cascade="all, delete-orphan", lazy="select")
    suggestions = relationship(
        "Suggestion",
        primaryjoin="BusinessRule.rule_id == foreign(Suggestion.rule_id)",
        viewonly=True,
        lazy="select"
    )


class BusinessRuleRepository:
    """Repository methods for BusinessRule table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        rule_id: str,
        project_id: int,
        content: str,
        version: str = "1.0.0",
        assumptions: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> BusinessRule:
        """Create a new business rule."""
        rule = BusinessRule(
            rule_id=rule_id,
            project_id=project_id,
            content=content,
            version=version,
            assumptions=assumptions,
            created_by=created_by
        )
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def get_by_id(self, rule_id: str) -> Optional[BusinessRule]:
        """Get business rule by rule_id."""
        return self.db.query(BusinessRule).filter(BusinessRule.rule_id == rule_id).first()

    def get_by_db_id(self, db_id: int) -> Optional[BusinessRule]:
        """Get business rule by database ID."""
        return self.db.query(BusinessRule).filter(BusinessRule.id == db_id).first()

    def get_by_project(
        self,
        project_id: int,
        status: Optional[RuleStatus] = None
    ) -> List[BusinessRule]:
        """Get all business rules for a project, optionally filtered by status."""
        query = self.db.query(BusinessRule).filter(BusinessRule.project_id == project_id)
        if status:
            query = query.filter(BusinessRule.status == status)
        return query.order_by(BusinessRule.created_at.desc()).all()

    def get_approved_by_project(self, project_id: int) -> List[BusinessRule]:
        """Get all approved business rules for a project."""
        return self.get_by_project(project_id, status=RuleStatus.APPROVED)

    def update_status(
        self,
        rule_id: str,
        status: RuleStatus,
        approved_by: Optional[str] = None
    ) -> Optional[BusinessRule]:
        """Update business rule status."""
        rule = self.get_by_id(rule_id)
        if not rule:
            return None
        
        rule.status = status
        if approved_by:
            rule.approved_by = approved_by
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def update(self, rule_id: str, **kwargs) -> Optional[BusinessRule]:
        """Update business rule fields."""
        rule = self.get_by_id(rule_id)
        if not rule:
            return None
        
        for key, value in kwargs.items():
            if hasattr(rule, key):
                setattr(rule, key, value)
        
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def delete(self, rule_id: str) -> bool:
        """Delete a business rule."""
        rule = self.get_by_id(rule_id)
        if not rule:
            return False
        
        self.db.delete(rule)
        self.db.commit()
        return True
