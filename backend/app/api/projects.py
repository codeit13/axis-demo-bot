"""Project API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, model_validator
from ..database import get_db
from ..tables import Project, CodeFile, ProjectRepository, CodeFileRepository

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    repository_url: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    repository_url: str
    created_at: str

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.isoformat()
        return self

    class Config:
        from_attributes = True


class CodeFileCreate(BaseModel):
    file_path: str
    content: str
    language: str = ""


class CodeFileResponse(BaseModel):
    id: int
    project_id: int
    file_path: str
    content: str
    language: str
    created_at: str
    updated_at: str

    @model_validator(mode='after')
    def convert_datetime(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            self.updated_at = self.updated_at.isoformat()
        return self

    class Config:
        from_attributes = True


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    repo = ProjectRepository(db)
    db_project = repo.create(
        name=project.name,
        description=project.description,
        repository_url=project.repository_url
    )
    project_dict = {
        "id": db_project.id,
        "name": db_project.name,
        "description": db_project.description or "",
        "repository_url": db_project.repository_url or "",
        "created_at": db_project.created_at.isoformat() if db_project.created_at else ""
    }
    return ProjectResponse(**project_dict)


@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    """List all projects."""
    repo = ProjectRepository(db)
    projects = repo.get_all()
    # Convert datetime to string for each project
    result = []
    for project in projects:
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description or "",
            "repository_url": project.repository_url or "",
            "created_at": project.created_at.isoformat() if project.created_at else ""
        }
        result.append(ProjectResponse(**project_dict))
    return result


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by ID."""
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_dict = {
        "id": project.id,
        "name": project.name,
        "description": project.description or "",
        "repository_url": project.repository_url or "",
        "created_at": project.created_at.isoformat() if project.created_at else ""
    }
    return ProjectResponse(**project_dict)


@router.post("/{project_id}/files", response_model=CodeFileResponse)
def create_code_file(
    project_id: int,
    file: CodeFileCreate,
    db: Session = Depends(get_db)
):
    """Create a code file for a project."""
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    file_repo = CodeFileRepository(db)
    code_file = file_repo.create(
        project_id=project_id,
        file_path=file.file_path,
        content=file.content,
        language=file.language or None
    )
    file_dict = {
        "id": code_file.id,
        "project_id": code_file.project_id,
        "file_path": code_file.file_path,
        "content": code_file.content,
        "language": code_file.language or "",
        "created_at": code_file.created_at.isoformat() if code_file.created_at else "",
        "updated_at": code_file.updated_at.isoformat() if code_file.updated_at else ""
    }
    return CodeFileResponse(**file_dict)


@router.get("/{project_id}/files", response_model=List[CodeFileResponse])
def list_code_files(project_id: int, db: Session = Depends(get_db)):
    """List all code files for a project."""
    file_repo = CodeFileRepository(db)
    files = file_repo.get_by_project(project_id)
    result = []
    for file in files:
        file_dict = {
            "id": file.id,
            "project_id": file.project_id,
            "file_path": file.file_path,
            "content": file.content,
            "language": file.language or "",
            "created_at": file.created_at.isoformat() if file.created_at else "",
            "updated_at": file.updated_at.isoformat() if file.updated_at else ""
        }
        result.append(CodeFileResponse(**file_dict))
    return result


@router.get("/{project_id}/files/{file_id}", response_model=CodeFileResponse)
def get_code_file(project_id: int, file_id: int, db: Session = Depends(get_db)):
    """Get code file by ID."""
    file_repo = CodeFileRepository(db)
    code_file = file_repo.get_by_id(file_id)
    if not code_file or code_file.project_id != project_id:
        raise HTTPException(status_code=404, detail="Code file not found")
    file_dict = {
        "id": code_file.id,
        "project_id": code_file.project_id,
        "file_path": code_file.file_path,
        "content": code_file.content,
        "language": code_file.language or "",
        "created_at": code_file.created_at.isoformat() if code_file.created_at else "",
        "updated_at": code_file.updated_at.isoformat() if code_file.updated_at else ""
    }
    return CodeFileResponse(**file_dict)
