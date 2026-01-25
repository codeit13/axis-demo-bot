"""Agent dependencies table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from typing import Optional, List
import json
from ..database import Base

# Import AgentType from suggestions module
from .suggestions import AgentType


class AgentDependency(Base):
    """Agent dependency tracking model."""
    __tablename__ = "agent_dependencies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_type = Column(SQLEnum(AgentType, native_enum=True), nullable=False, index=True)
    depends_on_rule_ids = Column(Text, nullable=True)  # JSON array
    depends_on_agent_types = Column(Text, nullable=True)  # JSON array
    created_at = Column(DateTime, default=func.now(), nullable=False)


class AgentDependencyRepository:
    """Repository methods for AgentDependency table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        agent_type: AgentType,
        depends_on_rule_ids: Optional[List[str]] = None,
        depends_on_agent_types: Optional[List[str]] = None
    ) -> AgentDependency:
        """Create a new agent dependency record."""
        dependency = AgentDependency(
            agent_type=agent_type,
            depends_on_rule_ids=json.dumps(depends_on_rule_ids) if depends_on_rule_ids else None,
            depends_on_agent_types=json.dumps(depends_on_agent_types) if depends_on_agent_types else None
        )
        self.db.add(dependency)
        self.db.commit()
        self.db.refresh(dependency)
        return dependency

    def get_by_id(self, dependency_id: int) -> Optional[AgentDependency]:
        """Get agent dependency by ID."""
        return self.db.query(AgentDependency).filter(AgentDependency.id == dependency_id).first()

    def get_by_agent_type(self, agent_type: AgentType) -> Optional[AgentDependency]:
        """Get dependency configuration for an agent type."""
        return self.db.query(AgentDependency).filter(AgentDependency.agent_type == agent_type).first()

    def get_all(self) -> List[AgentDependency]:
        """Get all agent dependencies."""
        return self.db.query(AgentDependency).all()

    def get_depends_on_rule_ids(self, dependency: AgentDependency) -> List[str]:
        """Parse and return depends_on_rule_ids from JSON."""
        if not dependency.depends_on_rule_ids:
            return []
        try:
            return json.loads(dependency.depends_on_rule_ids)
        except:
            return []

    def get_depends_on_agent_types(self, dependency: AgentDependency) -> List[str]:
        """Parse and return depends_on_agent_types from JSON."""
        if not dependency.depends_on_agent_types:
            return []
        try:
            return json.loads(dependency.depends_on_agent_types)
        except:
            return []

    def update(
        self,
        dependency_id: int,
        depends_on_rule_ids: Optional[List[str]] = None,
        depends_on_agent_types: Optional[List[str]] = None
    ) -> Optional[AgentDependency]:
        """Update agent dependency."""
        dependency = self.get_by_id(dependency_id)
        if not dependency:
            return None
        
        if depends_on_rule_ids is not None:
            dependency.depends_on_rule_ids = json.dumps(depends_on_rule_ids)
        if depends_on_agent_types is not None:
            dependency.depends_on_agent_types = json.dumps(depends_on_agent_types)
        
        self.db.commit()
        self.db.refresh(dependency)
        return dependency

    def delete(self, dependency_id: int) -> bool:
        """Delete an agent dependency."""
        dependency = self.get_by_id(dependency_id)
        if not dependency:
            return False
        
        self.db.delete(dependency)
        self.db.commit()
        return True
