"""Agent runs table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
from ..database import Base

# Import AgentType from suggestions module
from .suggestions import AgentType


class AgentRun(Base):
    """Agent execution history model."""
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_type = Column(SQLEnum(AgentType, native_enum=True), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    result_summary = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    triggered_by_rule_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", lazy="select")


class AgentRunRepository:
    """Repository methods for AgentRun table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        agent_type: AgentType,
        project_id: int,
        status: str,
        result_summary: Optional[str] = None,
        error_message: Optional[str] = None,
        triggered_by_rule_id: Optional[str] = None
    ) -> AgentRun:
        """Create a new agent run record."""
        agent_run = AgentRun(
            agent_type=agent_type,
            project_id=project_id,
            status=status,
            result_summary=result_summary,
            error_message=error_message,
            triggered_by_rule_id=triggered_by_rule_id
        )
        self.db.add(agent_run)
        self.db.commit()
        self.db.refresh(agent_run)
        return agent_run

    def get_by_id(self, run_id: int) -> Optional[AgentRun]:
        """Get agent run by ID."""
        return self.db.query(AgentRun).filter(AgentRun.id == run_id).first()

    def get_by_project(
        self,
        project_id: int,
        agent_type: Optional[AgentType] = None
    ) -> List[AgentRun]:
        """Get all agent runs for a project, optionally filtered by agent type."""
        query = self.db.query(AgentRun).filter(AgentRun.project_id == project_id)
        if agent_type:
            query = query.filter(AgentRun.agent_type == agent_type)
        return query.order_by(AgentRun.created_at.desc()).all()

    def get_latest_by_project_and_agent(
        self,
        project_id: int,
        agent_type: AgentType
    ) -> Optional[AgentRun]:
        """Get the latest agent run for a project and agent type."""
        return self.db.query(AgentRun).filter(
            AgentRun.project_id == project_id,
            AgentRun.agent_type == agent_type
        ).order_by(AgentRun.created_at.desc()).first()

    def delete(self, run_id: int) -> bool:
        """Delete an agent run."""
        agent_run = self.get_by_id(run_id)
        if not agent_run:
            return False
        
        self.db.delete(agent_run)
        self.db.commit()
        return True
