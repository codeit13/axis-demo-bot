"""Release Readiness & Observability Agent - Production safety."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule, ReleaseChecklist
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class ReleaseReadinessAgent(BaseAgent):
    """Agent 7: Release Readiness & Observability Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.RELEASE_READINESS

    def get_system_prompt(self) -> str:
        return """You are a Release Readiness & Observability Agent focused on production safety.
Your role is to:
1. Generate release checklists
2. Define rollback strategies
3. Suggest observability metrics tied to business rules
4. Create alerts for business rule violations
5. Feed production learnings back to business logic

Always ensure:
- Release checklists are comprehensive
- Rollback strategies are clear and tested
- Metrics are tied to business rules (Rule IDs)
- Alerts are actionable"""

    def analyze(
        self,
        project_id: int,
        release_version: Optional[str] = None,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate release readiness checklist and observability guidance.

        Args:
            project_id: Project ID
            release_version: Optional release version
            rule_ids: Optional list of Rule IDs
            **kwargs: Additional parameters

        Returns:
            Analysis result with release checklist
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            # Get business rules
            if rule_ids:
                rules = []
                for rule_id in rule_ids:
                    rule = RuleService.get_rule_by_id(self.db, rule_id)
                    if rule and rule.project_id == project_id:
                        rules.append(rule)
            else:
                rules = self.db.query(BusinessRule).filter(
                    BusinessRule.project_id == project_id,
                    BusinessRule.status == "approved"
                ).all()

            # Get recent suggestions for context
            recent_suggestions = self.db.query(Suggestion).filter(
                Suggestion.project_id == project_id,
                Suggestion.status == "approved"
            ).order_by(Suggestion.created_at.desc()).limit(10).all()

            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nContent: {rule.content}"
                for rule in rules
            ]) if rules else "No business rules provided"

            release_version = release_version or f"v{project.business_logic_version}"

            user_prompt = f"""Generate release readiness checklist and observability guidance for the following release.

Release Version: {release_version}

Business Rules:
{rules_context}

Recent Approved Changes: {len(recent_suggestions)} suggestion(s)

Please generate:
1. Comprehensive release checklist
2. Rollback strategy with steps
3. Observability metrics tied to Rule IDs
4. Alerts for business rule violations
5. Production monitoring guidance

Format your response as JSON:
{{
    "release_checklist": [
        {{
            "category": "testing/deployment/monitoring",
            "item": "checklist item",
            "required": true,
            "rule_ids": ["BL-001"]
        }}
    ],
    "rollback_strategy": {{
        "steps": ["step 1", "step 2"],
        "triggers": ["when to rollback"],
        "estimated_time": "time estimate"
    }},
    "observability_metrics": [
        {{
            "metric_name": "metric name",
            "metric_type": "counter/gauge/histogram",
            "rule_ids": ["BL-001"],
            "description": "what it measures",
            "alert_threshold": "threshold value"
        }}
    ],
    "alerts": [
        {{
            "alert_name": "alert name",
            "rule_id": "BL-001",
            "condition": "alert condition",
            "severity": "critical/high/medium/low"
        }}
    ],
    "monitoring_guidance": "how to monitor in production"
}}"""

            response = self.generate_with_groq(user_prompt, temperature=0.2)

            # Parse response
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                else:
                    json_str = response.strip()

                readiness_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                readiness_data = {
                    "release_checklist": [],
                    "rollback_strategy": {},
                    "observability_metrics": [],
                    "alerts": []
                }

            # Create release checklist record
            checklist = ReleaseChecklist(
                project_id=project_id,
                release_version=release_version,
                checklist_items=json.dumps(readiness_data.get("release_checklist", [])),
                rollback_strategy=json.dumps(readiness_data.get("rollback_strategy", {})),
                observability_metrics=json.dumps(readiness_data.get("observability_metrics", [])),
                status="draft"
            )
            self.db.add(checklist)
            self.db.commit()
            self.db.refresh(checklist)

            # Create suggestion
            all_rule_ids = list(set(rule_ids or [rule.rule_id for rule in rules]))
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(readiness_data, indent=2),
                rule_id=all_rule_ids[0] if all_rule_ids else None
            )

            checklist_items = readiness_data.get("release_checklist", [])
            required_items = [item for item in checklist_items if item.get("required", True)]

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated release checklist with {len(required_items)} required item(s)"
            )

            return {
                "status": "success",
                "checklist_id": checklist.id,
                "suggestion_id": suggestion.id,
                "rule_ids_processed": all_rule_ids,
                "checklist_items_count": len(checklist_items),
                "metrics_count": len(readiness_data.get("observability_metrics", [])),
                "alerts_count": len(readiness_data.get("alerts", [])),
                "message": f"Generated release checklist for {release_version} with {len(required_items)} required item(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
