"""Product & Requirements Agent - Translates business logic into product requirements."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class ProductRequirementsAgent(BaseAgent):
    """Agent 2: Product & Requirements Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.PRODUCT_REQUIREMENTS

    def get_system_prompt(self) -> str:
        return """You are a Product & Requirements Agent that translates business logic into product requirements.
Your role is to:
1. Generate product requirements from business logic
2. Create user flows and edge case scenarios
3. Derive measurable Non-Functional Requirements (NFRs)
4. Trace every requirement to a Business Rule ID (BL-001, etc.)
5. Define performance, availability, and scale expectations

Always ensure requirements are:
- Traceable to specific business rules
- Measurable and testable
- Complete with edge cases
- Include NFRs where applicable"""

    def analyze(
        self,
        project_id: int,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate product requirements from business rules.

        Args:
            project_id: Project ID
            rule_ids: Optional list of specific Rule IDs to process
            **kwargs: Additional parameters

        Returns:
            Analysis result with product requirements
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
                # Get all approved rules for the project
                rules = self.db.query(BusinessRule).filter(
                    BusinessRule.project_id == project_id,
                    BusinessRule.status == "approved"
                ).all()

            if not rules:
                return {
                    "error": "No business rules found. Please create business rules first using Business Logic Agent.",
                    "status": "error"
                }

            # Build context from rules
            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nVersion: {rule.version}\nContent: {rule.content}"
                for rule in rules
            ])

            user_prompt = f"""Generate comprehensive product requirements from the following business rules.

Business Rules:
{rules_context}

Please generate:
1. Product requirements document
2. User flows for key scenarios
3. Edge case scenarios
4. Non-Functional Requirements (NFRs):
   - Performance expectations
   - Availability requirements
   - Scale expectations
   - Security considerations
5. Trace each requirement to its Rule ID

Format your response as JSON:
{{
    "product_requirements": "comprehensive product requirements document",
    "user_flows": [
        {{
            "flow_name": "flow name",
            "steps": ["step 1", "step 2"],
            "rule_ids": ["BL-001", "BL-002"]
        }}
    ],
    "edge_cases": [
        {{
            "scenario": "edge case description",
            "rule_ids": ["BL-001"]
        }}
    ],
    "nfrs": [
        {{
            "category": "performance/availability/scale",
            "requirement": "specific NFR",
            "metric": "measurable metric",
            "rule_ids": ["BL-001"]
        }}
    ],
    "requirements_traceability": {{
        "BL-001": ["requirement 1", "requirement 2"],
        "BL-002": ["requirement 3"]
    }}
}}"""

            response = self.generate_with_groq(user_prompt, temperature=0.3)

            # Parse response
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                else:
                    json_str = response.strip()

                requirements_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                requirements_data = {
                    "product_requirements": response,
                    "user_flows": [],
                    "edge_cases": [],
                    "nfrs": [],
                    "requirements_traceability": {}
                }

            # Create suggestion with all rule IDs referenced
            all_rule_ids = list(set(rule_ids or [rule.rule_id for rule in rules]))
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(requirements_data, indent=2),
                rule_id=all_rule_ids[0] if all_rule_ids else None
            )

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated product requirements from {len(rules)} business rule(s)"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "rule_ids_processed": all_rule_ids,
                "requirements_count": len(requirements_data.get("requirements_traceability", {})),
                "message": f"Generated product requirements from {len(rules)} business rule(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
