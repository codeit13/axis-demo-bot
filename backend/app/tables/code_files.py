"""Code files table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
from ..database import Base


class CodeFile(Base):
    """Code file model."""
    __tablename__ = "code_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="code_files", lazy="select")
    suggestions = relationship("Suggestion", back_populates="code_file", lazy="select")


class CodeFileRepository:
    """Repository methods for CodeFile table."""

    def __init__(self, db):
        self.db = db

    def create(self, project_id: int, file_path: str, content: str, language: Optional[str] = None) -> CodeFile:
        """Create a new code file."""
        code_file = CodeFile(
            project_id=project_id,
            file_path=file_path,
            content=content,
            language=language
        )
        self.db.add(code_file)
        self.db.commit()
        self.db.refresh(code_file)
        return code_file

    def get_by_id(self, file_id: int) -> Optional[CodeFile]:
        """Get code file by ID."""
        return self.db.query(CodeFile).filter(CodeFile.id == file_id).first()

    def get_by_project(self, project_id: int) -> List[CodeFile]:
        """Get all code files for a project."""
        return self.db.query(CodeFile).filter(CodeFile.project_id == project_id).order_by(CodeFile.created_at.desc()).all()

    def get_by_project_and_path(self, project_id: int, file_path: str) -> Optional[CodeFile]:
        """Get code file by project ID and file path."""
        return self.db.query(CodeFile).filter(
            CodeFile.project_id == project_id,
            CodeFile.file_path == file_path
        ).first()

    def update(self, file_id: int, **kwargs) -> Optional[CodeFile]:
        """Update code file fields."""
        code_file = self.get_by_id(file_id)
        if not code_file:
            return None
        
        for key, value in kwargs.items():
            if hasattr(code_file, key):
                setattr(code_file, key, value)
        
        self.db.commit()
        self.db.refresh(code_file)
        return code_file

    def delete(self, file_id: int) -> bool:
        """Delete a code file."""
        code_file = self.get_by_id(file_id)
        if not code_file:
            return False
        
        self.db.delete(code_file)
        self.db.commit()
        return True
