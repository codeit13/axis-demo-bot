"""Business rule service for Rule ID generation and versioning."""
from sqlalchemy.orm import Session
from typing import Optional
from ..tables import BusinessRule, RuleVersion, Project
import re


class RuleService:
    """Service for managing business rules and Rule IDs."""

    @staticmethod
    def generate_rule_id(db: Session, project_id: int) -> str:
        """
        Generate next Rule ID (BL-001, BL-002, etc.).

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            Next available Rule ID
        """
        # Get the highest existing rule number for this project
        existing_rules = db.query(BusinessRule).filter(
            BusinessRule.project_id == project_id
        ).all()

        if not existing_rules:
            return "BL-001"

        # Extract numbers from existing rule IDs
        numbers = []
        for rule in existing_rules:
            match = re.search(r'BL-(\d+)', rule.rule_id)
            if match:
                numbers.append(int(match.group(1)))

        if not numbers:
            return "BL-001"

        next_num = max(numbers) + 1
        return f"BL-{next_num:03d}"

    @staticmethod
    def create_rule_version(
        db: Session,
        rule: BusinessRule,
        new_content: str,
        created_by: str,
        diff: Optional[str] = None
    ) -> RuleVersion:
        """
        Create a new version of a business rule.

        Args:
            db: Database session
            rule: Existing business rule
            new_content: New rule content
            created_by: User creating the version
            diff: Optional diff from previous version

        Returns:
            Created rule version
        """
        # Calculate next version (simple increment for now)
        current_version = rule.version
        try:
            major, minor, patch = map(int, current_version.split('.'))
            patch += 1
            new_version = f"{major}.{minor}.{patch}"
        except:
            new_version = "1.0.1"

        rule_version = RuleVersion(
            rule_id=rule.rule_id,
            version=new_version,
            content=new_content,
            diff=diff,
            created_by=created_by
        )
        db.add(rule_version)
        db.commit()
        db.refresh(rule_version)

        return rule_version

    @staticmethod
    def get_rule_by_id(db: Session, rule_id: str) -> Optional[BusinessRule]:
        """Get business rule by Rule ID."""
        return db.query(BusinessRule).filter(BusinessRule.rule_id == rule_id).first()

    @staticmethod
    def get_rule_versions(db: Session, rule_id: str) -> list:
        """Get all versions of a rule."""
        return db.query(RuleVersion).filter(
            RuleVersion.rule_id == rule_id
        ).order_by(RuleVersion.created_at.desc()).all()

    @staticmethod
    def detect_conflicts(db: Session, project_id: int, new_content: str) -> list:
        """
        Detect potential conflicts with existing rules.

        Args:
            db: Database session
            project_id: Project ID
            new_content: New rule content to check

        Returns:
            List of potential conflicts
        """
        existing_rules = db.query(BusinessRule).filter(
            BusinessRule.project_id == project_id,
            BusinessRule.status.in_(["approved", "pending_approval"])
        ).all()

        conflicts = []
        # Simple keyword-based conflict detection
        # In production, this would use more sophisticated NLP
        # Ensure new_content is a string
        if not isinstance(new_content, str):
            if isinstance(new_content, dict):
                new_content = str(new_content)
            else:
                new_content = str(new_content) if new_content else ""
        
        new_keywords = set(re.findall(r'\b\w+\b', new_content.lower()))

        for rule in existing_rules:
            # Ensure rule.content is a string
            rule_content = rule.content
            if not isinstance(rule_content, str):
                rule_content = str(rule_content) if rule_content else ""
            rule_keywords = set(re.findall(r'\b\w+\b', rule_content.lower()))
            overlap = new_keywords.intersection(rule_keywords)
            if len(overlap) > 5:  # Threshold for potential conflict
                conflicts.append({
                    "rule_id": rule.rule_id,
                    "version": rule.version,
                    "overlap_keywords": list(overlap)
                })

        return conflicts
