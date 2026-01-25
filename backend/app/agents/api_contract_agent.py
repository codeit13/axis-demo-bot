"""API & Contract Agent - Defines system contracts."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class APIContractAgent(BaseAgent):
    """Agent 3: API & Contract Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.API_CONTRACT

    def get_system_prompt(self) -> str:
        return """You are an API & Contract Agent that defines system contracts.
Your role is to:
1. Generate OpenAPI/Swagger specifications
2. Define gRPC contracts if needed
3. Enforce backward compatibility
4. Define versioning strategy
5. Annotate endpoints with Business Rule IDs (BL-001, etc.)
6. Identify breaking changes

Always ensure:
- Contracts are backward compatible when possible
- Breaking changes are clearly marked
- All endpoints trace to business rules
- Versioning strategy is explicit"""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate API contracts from business rules and/or code.

        Args:
            project_id: Project ID
            code_file_id: Optional code file to analyze
            rule_ids: Optional list of Rule IDs
            **kwargs: Additional parameters

        Returns:
            Analysis result with API contracts
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

            # Get code files if provided
            code_context = ""
            if code_file_id:
                code_file = self.get_code_file(code_file_id)
                if code_file:
                    code_context = f"\n\nExisting Code:\n```{code_file.language or ''}\n{code_file.content}\n```"
            else:
                # Get all code files for context
                code_files = self.get_project_code_files(project_id)
                if code_files:
                    code_context = "\n\nExisting Code Files:\n"
                    for cf in code_files[:3]:  # Limit to first 3 files
                        code_context += f"\nFile: {cf.file_path}\n```{cf.language or ''}\n{cf.content[:500]}...\n```"

            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nContent: {rule.content}"
                for rule in rules
            ]) if rules else "No business rules provided"

            user_prompt = f"""Generate comprehensive API contracts from the following business rules and code.

Business Rules:
{rules_context}
{code_context}

Please generate:
1. Complete OpenAPI 3.0 specification
2. All endpoints with request/response schemas
3. Annotate each endpoint with relevant Rule IDs (e.g., BL-001)
4. Versioning strategy
5. Backward compatibility analysis
6. Breaking changes (if any) - clearly marked
7. Consumer compatibility considerations

Format your response as JSON:
{{
    "openapi_spec": "complete OpenAPI YAML specification",
    "endpoints": [
        {{
            "path": "/api/endpoint",
            "method": "GET/POST/etc",
            "rule_ids": ["BL-001", "BL-002"],
            "description": "endpoint description",
            "breaking_change": false
        }}
    ],
    "versioning_strategy": "versioning approach",
    "backward_compatibility": "compatibility analysis",
    "breaking_changes": ["list of breaking changes if any"],
    "consumer_considerations": ["internal consumer considerations"]
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

                contract_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                contract_data = {
                    "openapi_spec": response,
                    "endpoints": [],
                    "versioning_strategy": "semantic versioning",
                    "breaking_changes": []
                }

            # Create suggestion
            all_rule_ids = list(set(rule_ids or [rule.rule_id for rule in rules]))
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(contract_data, indent=2),
                code_file_id=code_file_id,
                rule_id=all_rule_ids[0] if all_rule_ids else None
            )

            breaking_changes = contract_data.get("breaking_changes", [])
            requires_approval = len(breaking_changes) > 0

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated API contracts with {len(contract_data.get('endpoints', []))} endpoint(s)"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "rule_ids_processed": all_rule_ids,
                "endpoints_count": len(contract_data.get("endpoints", [])),
                "breaking_changes": breaking_changes,
                "requires_approval": requires_approval,
                "message": f"Generated API contracts. {'⚠️ Breaking changes detected - human approval required.' if requires_approval else ''}"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
