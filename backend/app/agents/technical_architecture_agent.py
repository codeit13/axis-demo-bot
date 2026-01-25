"""Technical Architecture Agent - Technical design without code generation."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class TechnicalArchitectureAgent(BaseAgent):
    """Agent 4: Technical Architecture Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.TECHNICAL_ARCHITECTURE

    def get_system_prompt(self) -> str:
        return """You are a Technical Architecture Agent that designs technical solutions.
Your role is to:
1. Recommend tech stack and architectural patterns
2. Define data models and schemas
3. Plan migration strategies
4. Flag risky changes and scaling bottlenecks
5. Provide integration guidance

IMPORTANT: You do NOT generate production code. You provide:
- Architecture diagrams (in text/markdown)
- Data model definitions
- Technology recommendations
- Migration plans
- Risk assessments

Always ensure recommendations are:
- Aligned with business rules
- Scalable and maintainable
- Risk-aware"""

    def analyze(
        self,
        project_id: int,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate technical architecture recommendations.

        Args:
            project_id: Project ID
            rule_ids: Optional list of Rule IDs
            **kwargs: Additional parameters

        Returns:
            Analysis result with architecture recommendations
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

            # Get existing code files for context
            code_files = self.get_project_code_files(project_id)
            existing_tech_stack = ""
            if code_files:
                languages = set(cf.language for cf in code_files if cf.language)
                existing_tech_stack = f"\n\nExisting Tech Stack: {', '.join(languages) if languages else 'Unknown'}"

            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nContent: {rule.content}"
                for rule in rules
            ]) if rules else "No business rules provided"

            user_prompt = f"""Design technical architecture based on the following business rules.

Business Rules:
{rules_context}
{existing_tech_stack}

Please provide:
1. Tech stack recommendations (languages, frameworks, databases, etc.)
2. Architectural patterns (microservices, monolith, event-driven, etc.)
3. Data model definitions (schemas, relationships)
4. Migration strategies (if applicable)
5. Integration guidance
6. Risk assessment:
   - Risky changes
   - Scaling bottlenecks
   - Performance concerns
7. Link recommendations to Rule IDs

IMPORTANT: Do NOT generate production code. Provide architecture and design only.

Format your response as JSON:
{{
    "tech_stack": {{
        "languages": ["language 1", "language 2"],
        "frameworks": ["framework 1"],
        "databases": ["database 1"],
        "reasoning": "why these choices"
    }},
    "architectural_patterns": "recommended patterns",
    "data_models": [
        {{
            "model_name": "model name",
            "schema": "schema definition",
            "rule_ids": ["BL-001"]
        }}
    ],
    "migration_strategy": "migration plan if applicable",
    "integration_guidance": "how to integrate components",
    "risks": [
        {{
            "risk": "risk description",
            "severity": "high/medium/low",
            "mitigation": "how to mitigate"
        }}
    ],
    "scaling_considerations": "scaling strategy",
    "rule_traceability": {{
        "BL-001": ["architectural decision 1"]
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

                architecture_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                architecture_data = {
                    "tech_stack": {},
                    "architectural_patterns": response,
                    "data_models": [],
                    "risks": []
                }

            # Create suggestion
            all_rule_ids = list(set(rule_ids or [rule.rule_id for rule in rules]))
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(architecture_data, indent=2),
                rule_id=all_rule_ids[0] if all_rule_ids else None
            )

            risks = architecture_data.get("risks", [])
            high_risks = [r for r in risks if r.get("severity", "").lower() == "high"]

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated technical architecture with {len(risks)} risk(s) identified"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "rule_ids_processed": all_rule_ids,
                "risks_count": len(risks),
                "high_risks_count": len(high_risks),
                "message": f"Generated technical architecture. {len(high_risks)} high-risk item(s) identified."
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
