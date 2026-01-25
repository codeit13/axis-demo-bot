"""Approvals table schema, types, and repository methods."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional, List
from ..database import Base


class Approval(Base):
    """Human approval/rejection model."""
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    suggestion_id = Column(Integer, ForeignKey("suggestions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_action = Column(String(50), nullable=False)
    comments = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    suggestion = relationship("Suggestion", back_populates="approvals", lazy="select")


class ApprovalRepository:
    """Repository methods for Approval table."""

    def __init__(self, db):
        self.db = db

    def create(
        self,
        suggestion_id: int,
        user_action: str,
        comments: Optional[str] = None
    ) -> Approval:
        """Create a new approval record."""
        approval = Approval(
            suggestion_id=suggestion_id,
            user_action=user_action,
            comments=comments
        )
        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)
        return approval

    def get_by_id(self, approval_id: int) -> Optional[Approval]:
        """Get approval by ID."""
        return self.db.query(Approval).filter(Approval.id == approval_id).first()

    def get_by_suggestion(self, suggestion_id: int) -> List[Approval]:
        """Get all approvals for a suggestion."""
        return self.db.query(Approval).filter(
            Approval.suggestion_id == suggestion_id
        ).order_by(Approval.timestamp.desc()).all()

    def get_latest_by_suggestion(self, suggestion_id: int) -> Optional[Approval]:
        """Get the latest approval for a suggestion."""
        return self.db.query(Approval).filter(
            Approval.suggestion_id == suggestion_id
        ).order_by(Approval.timestamp.desc()).first()

    def delete(self, approval_id: int) -> bool:
        """Delete an approval."""
        approval = self.get_by_id(approval_id)
        if not approval:
            return False
        
        self.db.delete(approval)
        self.db.commit()
        return True
