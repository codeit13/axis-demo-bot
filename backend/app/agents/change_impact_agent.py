"""Change Impact & Drift Agent - Prevents silent breakage."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, ChangeType, ChangeImpact, RiskLevel, BusinessRule, Suggestion
from ..services.groq_service import GroqService
from ..services.orchestration_service import OrchestrationService


class ChangeImpactAgent(BaseAgent):
    """Agent 6: Change Impact & Drift Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.CHANGE_IMPACT

    def get_system_prompt(self) -> str:
        return """You are a Change Impact & Drift Agent that prevents silent breakage.
Your role is to:
1. Detect architecture drift
2. Check spec vs code consistency
3. Analyze change impacts
4. Identify which agents need re-running
5. Produce human review checklists

Always ensure:
- All impacts are identified
- Required re-runs are clear
- Risks are properly assessed
- Human review items are actionable"""

    def analyze(
        self,
        project_id: int,
        change_type: Optional[str] = None,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze change impact and detect drift.

        Args:
            project_id: Project ID
            change_type: Type of change (business_rule_update, api_contract_change, etc.)
            rule_ids: Optional list of affected Rule IDs
            **kwargs: Additional parameters

        Returns:
            Analysis result with impact assessment
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            # Determine change type
            if change_type:
                try:
                    change_enum = ChangeType(change_type)
                except ValueError:
                    change_enum = ChangeType.BUSINESS_RULE_UPDATE
            else:
                change_enum = ChangeType.BUSINESS_RULE_UPDATE

            # Get affected rules
            if rule_ids:
                affected_rules = []
                for rule_id in rule_ids:
                    rule = self.db.query(BusinessRule).filter(
                        BusinessRule.rule_id == rule_id,
                        BusinessRule.project_id == project_id
                    ).first()
                    if rule:
                        affected_rules.append(rule)
            else:
                # Get recent rule changes
                affected_rules = self.db.query(BusinessRule).filter(
                    BusinessRule.project_id == project_id,
                    BusinessRule.status.in_(["pending_approval", "approved"])
                ).order_by(BusinessRule.updated_at.desc()).limit(5).all()

            # Get existing suggestions to check for drift
            existing_suggestions = self.db.query(Suggestion).filter(
                Suggestion.project_id == project_id
            ).order_by(Suggestion.created_at.desc()).limit(10).all()

            # Get code files for consistency check
            code_files = self.get_project_code_files(project_id)

            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nVersion: {rule.version}\nContent: {rule.content}"
                for rule in affected_rules
            ]) if affected_rules else "No specific rules provided"

            user_prompt = f"""Analyze the impact of the following change and detect any drift.

Change Type: {change_enum.value}

Affected Business Rules:
{rules_context}

Existing Suggestions Count: {len(existing_suggestions)}
Code Files Count: {len(code_files)}

Please analyze:
1. Impact on product requirements
2. Impact on API contracts
3. Impact on tests
4. Architecture drift detection
5. Spec vs code consistency
6. Which agents need re-running
7. Risk assessment
8. Human review checklist

Format your response as JSON:
{{
    "impact_analysis": {{
        "product_requirements": "impact on requirements",
        "api_contracts": "impact on APIs",
        "tests": "impact on tests",
        "architecture": "impact on architecture"
    }},
    "drift_detected": [
        {{
            "type": "architecture/spec/code",
            "description": "what drift was detected",
            "severity": "high/medium/low"
        }}
    ],
    "consistency_issues": [
        {{
            "issue": "consistency issue",
            "severity": "high/medium/low"
        }}
    ],
    "required_agent_reruns": ["agent type 1", "agent type 2"],
    "risk_assessment": {{
        "overall_risk": "low/medium/high/critical",
        "risks": [
            {{
                "risk": "risk description",
                "severity": "high/medium/low",
                "mitigation": "how to mitigate"
            }}
        ]
    }},
    "human_review_checklist": [
        "review item 1",
        "review item 2"
    ]
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

                impact_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                impact_data = {
                    "impact_analysis": {},
                    "drift_detected": [],
                    "required_agent_reruns": [],
                    "risk_assessment": {"overall_risk": "medium"}
                }

            # Use orchestration service to determine affected agents
            affected_agents = OrchestrationService.get_affected_agents(change_enum)
            required_reruns = OrchestrationService.get_execution_order(affected_agents)

            # Determine risk level
            risk_str = impact_data.get("risk_assessment", {}).get("overall_risk", "medium").lower()
            risk_level = RiskLevel.MEDIUM
            if risk_str == "critical":
                risk_level = RiskLevel.CRITICAL
            elif risk_str == "high":
                risk_level = RiskLevel.HIGH
            elif risk_str == "low":
                risk_level = RiskLevel.LOW

            # Create change impact record
            change_impact = ChangeImpact(
                project_id=project_id,
                change_type=change_enum,
                affected_rule_ids=json.dumps(rule_ids or [r.rule_id for r in affected_rules]),
                affected_agents=json.dumps([a.value for a in affected_agents]),
                required_reruns=json.dumps([a.value for a in required_reruns]),
                risk_level=risk_level,
                analysis_result=json.dumps(impact_data, indent=2)
            )
            self.db.add(change_impact)
            self.db.commit()
            self.db.refresh(change_impact)

            # Create suggestion
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(impact_data, indent=2),
                rule_id=rule_ids[0] if rule_ids else None
            )

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Analyzed change impact: {len(required_reruns)} agent(s) need re-running"
            )

            return {
                "status": "success",
                "change_impact_id": change_impact.id,
                "suggestion_id": suggestion.id,
                "affected_agents": [a.value for a in affected_agents],
                "required_reruns": [a.value for a in required_reruns],
                "risk_level": risk_level.value,
                "drift_detected": len(impact_data.get("drift_detected", [])),
                "message": f"Change impact analyzed. {len(required_reruns)} agent(s) need re-running."
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
