"""Rule versions table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
from ..database import Base


class RuleVersion(Base):
    """Business rule version history model."""
    __tablename__ = "rule_versions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_id = Column(String(50), ForeignKey("business_rules.rule_id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    diff = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=True)

    # Relationships
    rule = relationship("BusinessRule", back_populates="versions", lazy="select")


class RuleVersionRepository:
    """Repository methods for RuleVersion table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        rule_id: str,
        version: str,
        content: str,
        diff: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> RuleVersion:
        """Create a new rule version."""
        rule_version = RuleVersion(
            rule_id=rule_id,
            version=version,
            content=content,
            diff=diff,
            created_by=created_by
        )
        self.db.add(rule_version)
        self.db.commit()
        self.db.refresh(rule_version)
        return rule_version

    def get_by_id(self, version_id: int) -> Optional[RuleVersion]:
        """Get rule version by ID."""
        return self.db.query(RuleVersion).filter(RuleVersion.id == version_id).first()

    def get_by_rule_id(self, rule_id: str) -> List[RuleVersion]:
        """Get all versions for a rule."""
        return self.db.query(RuleVersion).filter(
            RuleVersion.rule_id == rule_id
        ).order_by(RuleVersion.created_at.desc()).all()

    def get_by_rule_and_version(self, rule_id: str, version: str) -> Optional[RuleVersion]:
        """Get a specific version of a rule."""
        return self.db.query(RuleVersion).filter(
            RuleVersion.rule_id == rule_id,
            RuleVersion.version == version
        ).first()

    def delete(self, version_id: int) -> bool:
        """Delete a rule version."""
        rule_version = self.get_by_id(version_id)
        if not rule_version:
            return False
        
        self.db.delete(rule_version)
        self.db.commit()
        return True
