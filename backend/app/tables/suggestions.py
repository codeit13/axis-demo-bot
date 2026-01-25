"""Suggestions table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
import enum
from ..database import Base


class AgentType(str, enum.Enum):
    """Agent type enumeration."""
    BUSINESS_LOGIC_POLICY = "business_logic_policy"
    PRODUCT_REQUIREMENTS = "product_requirements"
    API_CONTRACT = "api_contract"
    TECHNICAL_ARCHITECTURE = "technical_architecture"
    QUALITY_TEST = "quality_test"
    CHANGE_IMPACT = "change_impact"
    RELEASE_READINESS = "release_readiness"
    # Demo/UI agents
    INTEGRATION_AGENT = "integration_agent"
    CODE_TEMPLATE_AGENT = "code_template_agent"
    PROMPT_AMPLIFIER_AGENT = "prompt_amplifier_agent"
    # Legacy agents
    UNIT_TEST = "unit_test"
    API_SPEC = "api_spec"
    BUSINESS_LOGIC = "business_logic"
    BUG_SCANNER = "bug_scanner"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"


class SuggestionStatus(str, enum.Enum):
    """Suggestion status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Suggestion(Base):
    """AI agent suggestion model."""
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_type = Column(SQLEnum(AgentType, native_enum=True), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    code_file_id = Column(Integer, ForeignKey("code_files.id", ondelete="SET NULL"), nullable=True)
    issue_id = Column(Integer, ForeignKey("issues.id", ondelete="SET NULL"), nullable=True)
    rule_id = Column(String(50), nullable=True, index=True)
    version = Column(String(50), nullable=True)
    parent_suggestion_id = Column(Integer, ForeignKey("suggestions.id", ondelete="SET NULL"), nullable=True)
    content = Column(Text, nullable=False)
    status = Column(SQLEnum(SuggestionStatus), default=SuggestionStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="suggestions", lazy="select")
    code_file = relationship("CodeFile", back_populates="suggestions", lazy="select")
    issue = relationship("Issue", back_populates="suggestions", lazy="select")
    approvals = relationship("Approval", back_populates="suggestion", cascade="all, delete-orphan", lazy="select")
    parent_suggestion = relationship("Suggestion", remote_side=[id], backref="child_suggestions", lazy="select")
    business_rule = relationship(
        "BusinessRule",
        primaryjoin="foreign(Suggestion.rule_id) == BusinessRule.rule_id",
        viewonly=True,
        lazy="select"
    )


class SuggestionRepository:
    """Repository methods for Suggestion table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        agent_type: AgentType,
        project_id: int,
        content: str,
        code_file_id: Optional[int] = None,
        issue_id: Optional[int] = None,
        rule_id: Optional[str] = None,
        version: Optional[str] = None,
        parent_suggestion_id: Optional[int] = None
    ) -> Suggestion:
        """Create a new suggestion."""
        suggestion = Suggestion(
            agent_type=agent_type,
            project_id=project_id,
            content=content,
            code_file_id=code_file_id,
            issue_id=issue_id,
            rule_id=rule_id,
            version=version,
            parent_suggestion_id=parent_suggestion_id
        )
        self.db.add(suggestion)
        self.db.commit()
        self.db.refresh(suggestion)
        return suggestion

    def get_by_id(self, suggestion_id: int) -> Optional[Suggestion]:
        """Get suggestion by ID."""
        return self.db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()

    def get_by_project(
        self,
        project_id: int,
        agent_type: Optional[AgentType] = None,
        status: Optional[SuggestionStatus] = None
    ) -> List[Suggestion]:
        """Get all suggestions for a project, optionally filtered."""
        query = self.db.query(Suggestion).filter(Suggestion.project_id == project_id)
        if agent_type:
            query = query.filter(Suggestion.agent_type == agent_type)
        if status:
            query = query.filter(Suggestion.status == status)
        return query.order_by(Suggestion.created_at.desc()).all()

    def get_by_rule_id(self, rule_id: str) -> List[Suggestion]:
        """Get all suggestions for a rule ID."""
        return self.db.query(Suggestion).filter(Suggestion.rule_id == rule_id).order_by(Suggestion.created_at.desc()).all()

    def update_status(self, suggestion_id: int, status: SuggestionStatus) -> Optional[Suggestion]:
        """Update suggestion status."""
        suggestion = self.get_by_id(suggestion_id)
        if not suggestion:
            return None
        
        suggestion.status = status
        self.db.commit()
        self.db.refresh(suggestion)
        return suggestion

    def update(self, suggestion_id: int, **kwargs) -> Optional[Suggestion]:
        """Update suggestion fields."""
        suggestion = self.get_by_id(suggestion_id)
        if not suggestion:
            return None
        
        for key, value in kwargs.items():
            if hasattr(suggestion, key):
                setattr(suggestion, key, value)
        
        self.db.commit()
        self.db.refresh(suggestion)
        return suggestion

    def delete(self, suggestion_id: int) -> bool:
        """Delete a suggestion."""
        suggestion = self.get_by_id(suggestion_id)
        if not suggestion:
            return False
        
        self.db.delete(suggestion)
        self.db.commit()
        return True
