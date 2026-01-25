"""Mock Bitbucket API service."""
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..tables import Issue, IssueStatus


class BitbucketMockService:
    """Mock Bitbucket API service for demo purposes."""

    @staticmethod
    def create_issue(
        db: Session,
        project_id: int,
        title: str,
        description: str,
        code_file_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a mock Bitbucket issue.

        Args:
            db: Database session
            project_id: Project ID
            title: Issue title
            description: Issue description
            code_file_id: Optional code file ID

        Returns:
            Dictionary with issue data including mock Bitbucket ID
        """
        # Generate mock Bitbucket issue ID
        bitbucket_id = f"BB-{uuid.uuid4().hex[:8].upper()}"

        # Create issue in database
        issue = Issue(
            project_id=project_id,
            title=title,
            description=description,
            status=IssueStatus.OPEN,
            bitbucket_issue_id=bitbucket_id
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)

        return {
            "id": issue.id,
            "bitbucket_issue_id": bitbucket_id,
            "title": title,
            "description": description,
            "status": issue.status.value,
            "created_at": issue.created_at.isoformat(),
            "project_id": project_id
        }

    @staticmethod
    def get_issue(db: Session, issue_id: int) -> Optional[Dict[str, Any]]:
        """
        Get issue by ID.

        Args:
            db: Database session
            issue_id: Issue ID

        Returns:
            Issue data dictionary or None
        """
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return None

        return {
            "id": issue.id,
            "bitbucket_issue_id": issue.bitbucket_issue_id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status.value,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "project_id": issue.project_id
        }

    @staticmethod
    def update_issue_status(
        db: Session,
        issue_id: int,
        status: IssueStatus
    ) -> Optional[Dict[str, Any]]:
        """
        Update issue status.

        Args:
            db: Database session
            issue_id: Issue ID
            status: New status

        Returns:
            Updated issue data or None
        """
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return None

        issue.status = status
        issue.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(issue)

        return {
            "id": issue.id,
            "bitbucket_issue_id": issue.bitbucket_issue_id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status.value,
            "updated_at": issue.updated_at.isoformat()
        }

    @staticmethod
    def list_issues(db: Session, project_id: Optional[int] = None) -> list:
        """
        List all issues, optionally filtered by project.

        Args:
            db: Database session
            project_id: Optional project ID filter

        Returns:
            List of issue dictionaries
        """
        query = db.query(Issue)
        if project_id:
            query = query.filter(Issue.project_id == project_id)

        issues = query.all()
        return [
            {
                "id": issue.id,
                "bitbucket_issue_id": issue.bitbucket_issue_id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status.value,
                "created_at": issue.created_at.isoformat(),
                "project_id": issue.project_id
            }
            for issue in issues
        ]
