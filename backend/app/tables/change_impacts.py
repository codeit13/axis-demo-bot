"""Change impacts table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
import enum
import json
from ..database import Base


class ChangeType(str, enum.Enum):
    """Change type enumeration."""
    BUSINESS_RULE_UPDATE = "business_rule_update"
    API_CONTRACT_CHANGE = "api_contract_change"
    CODE_CHANGE = "code_change"
    ARCHITECTURE_CHANGE = "architecture_change"


class RiskLevel(str, enum.Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ChangeImpact(Base):
    """Change impact analysis model."""
    __tablename__ = "change_impacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(SQLEnum(ChangeType), nullable=False)
    affected_rule_ids = Column(Text, nullable=True)  # JSON array
    affected_agents = Column(Text, nullable=True)  # JSON array
    required_reruns = Column(Text, nullable=True)  # JSON array
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.MEDIUM, nullable=False)
    analysis_result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", lazy="select")


class ChangeImpactRepository:
    """Repository methods for ChangeImpact table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        project_id: int,
        change_type: ChangeType,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        affected_rule_ids: Optional[List[str]] = None,
        affected_agents: Optional[List[str]] = None,
        required_reruns: Optional[List[str]] = None,
        analysis_result: Optional[str] = None
    ) -> ChangeImpact:
        """Create a new change impact record."""
        change_impact = ChangeImpact(
            project_id=project_id,
            change_type=change_type,
            risk_level=risk_level,
            affected_rule_ids=json.dumps(affected_rule_ids) if affected_rule_ids else None,
            affected_agents=json.dumps(affected_agents) if affected_agents else None,
            required_reruns=json.dumps(required_reruns) if required_reruns else None,
            analysis_result=analysis_result
        )
        self.db.add(change_impact)
        self.db.commit()
        self.db.refresh(change_impact)
        return change_impact

    def get_by_id(self, impact_id: int) -> Optional[ChangeImpact]:
        """Get change impact by ID."""
        return self.db.query(ChangeImpact).filter(ChangeImpact.id == impact_id).first()

    def get_by_project(self, project_id: int) -> List[ChangeImpact]:
        """Get all change impacts for a project."""
        return self.db.query(ChangeImpact).filter(
            ChangeImpact.project_id == project_id
        ).order_by(ChangeImpact.created_at.desc()).all()

    def get_by_project_and_type(
        self,
        project_id: int,
        change_type: ChangeType
    ) -> List[ChangeImpact]:
        """Get change impacts by project and change type."""
        return self.db.query(ChangeImpact).filter(
            ChangeImpact.project_id == project_id,
            ChangeImpact.change_type == change_type
        ).order_by(ChangeImpact.created_at.desc()).all()

    def get_affected_rule_ids(self, impact: ChangeImpact) -> List[str]:
        """Parse and return affected rule IDs from JSON."""
        if not impact.affected_rule_ids:
            return []
        try:
            return json.loads(impact.affected_rule_ids)
        except:
            return []

    def get_affected_agents(self, impact: ChangeImpact) -> List[str]:
        """Parse and return affected agents from JSON."""
        if not impact.affected_agents:
            return []
        try:
            return json.loads(impact.affected_agents)
        except:
            return []

    def get_required_reruns(self, impact: ChangeImpact) -> List[str]:
        """Parse and return required reruns from JSON."""
        if not impact.required_reruns:
            return []
        try:
            return json.loads(impact.required_reruns)
        except:
            return []

    def delete(self, impact_id: int) -> bool:
        """Delete a change impact."""
        change_impact = self.get_by_id(impact_id)
        if not change_impact:
            return False
        
        self.db.delete(change_impact)
        self.db.commit()
        return True
