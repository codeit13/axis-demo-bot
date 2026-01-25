"""Base agent class for all AI agents."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from ..tables import AgentType, Suggestion, SuggestionStatus, Project, CodeFile, AgentRun
from ..services.groq_service import GroqService
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, db: Session):
        """
        Initialize agent.

        Args:
            db: Database session
        """
        self.db = db
        self.groq_service = GroqService()
        self.agent_type = self.get_agent_type()

    @abstractmethod
    def get_agent_type(self) -> AgentType:
        """Return the agent type."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    def analyze(self, project_id: int, **kwargs) -> Dict[str, Any]:
        """
        Perform analysis and generate suggestions.

        Args:
            project_id: Project ID to analyze
            **kwargs: Additional agent-specific parameters

        Returns:
            Dictionary with analysis results
        """
        pass

    def create_suggestion(
        self,
        project_id: int,
        content: str,
        code_file_id: Optional[int] = None,
        issue_id: Optional[int] = None,
        rule_id: Optional[str] = None,
        version: Optional[str] = None,
        parent_suggestion_id: Optional[int] = None
    ) -> Suggestion:
        """
        Create a suggestion in the database.

        Args:
            project_id: Project ID
            content: Suggestion content (can be JSON string)
            code_file_id: Optional code file ID
            issue_id: Optional issue ID
            rule_id: Optional Rule ID (e.g., BL-001)
            version: Optional version string
            parent_suggestion_id: Optional parent suggestion ID for cascading changes

        Returns:
            Created suggestion object
        """
        suggestion = Suggestion(
            agent_type=self.agent_type,
            project_id=project_id,
            code_file_id=code_file_id,
            issue_id=issue_id,
            rule_id=rule_id,
            version=version,
            parent_suggestion_id=parent_suggestion_id,
            content=content,
            status=SuggestionStatus.PENDING
        )
        self.db.add(suggestion)
        self.db.commit()
        self.db.refresh(suggestion)
        return suggestion

    def log_agent_run(
        self,
        project_id: int,
        status: str,
        result_summary: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> AgentRun:
        """
        Log agent execution.

        Args:
            project_id: Project ID
            status: Run status ("success", "error", "pending")
            result_summary: Optional summary of results
            error_message: Optional error message

        Returns:
            Created agent run object
        """
        agent_run = AgentRun(
            agent_type=self.agent_type,
            project_id=project_id,
            status=status,
            result_summary=result_summary,
            error_message=error_message
        )
        self.db.add(agent_run)
        self.db.commit()
        self.db.refresh(agent_run)
        return agent_run

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_code_file(self, code_file_id: int) -> Optional[CodeFile]:
        """Get code file by ID."""
        return self.db.query(CodeFile).filter(CodeFile.id == code_file_id).first()

    def get_project_code_files(self, project_id: int) -> List[CodeFile]:
        """Get all code files for a project."""
        return self.db.query(CodeFile).filter(CodeFile.project_id == project_id).all()

    def generate_with_groq(
        self,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response using Groq API.

        Args:
            user_prompt: User prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens

        Returns:
            Generated text
        """
        return self.groq_service.generate(
            system_prompt=self.get_system_prompt(),
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
