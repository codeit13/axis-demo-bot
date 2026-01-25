"""Quality & Test Intelligence Agent - Validates correctness against business intent."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class QualityTestAgent(BaseAgent):
    """Agent 5: Quality & Test Intelligence Agent."""

    def get_agent_type(self) -> AgentType:
        return AgentType.QUALITY_TEST

    def get_system_prompt(self) -> str:
        return """You are a Quality & Test Intelligence Agent that validates correctness.
Your role is to:
1. Generate test cases mapped to Business Rule IDs (BL-001, etc.)
2. Detect missing test coverage
3. Validate that business logic is enforced in code
4. Ensure code changes align with business rules
5. Provide integration and regression test strategies

Always ensure:
- Every test case traces to a Rule ID
- Coverage is comprehensive (normal, edge, error cases)
- Business rules are validated in tests
- Missing coverage is identified"""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        rule_ids: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate tests mapped to business rules.

        Args:
            project_id: Project ID
            code_file_id: Optional specific code file
            rule_ids: Optional list of Rule IDs
            **kwargs: Additional parameters

        Returns:
            Analysis result with test cases
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

            if not rules:
                return {
                    "error": "No business rules found. Please create business rules first.",
                    "status": "error"
                }

            # Get code files
            if code_file_id:
                code_file = self.get_code_file(code_file_id)
                code_files = [code_file] if code_file else []
            else:
                code_files = self.get_project_code_files(project_id)

            if not code_files:
                return {"error": "No code files found in project", "status": "error"}

            rules_context = "\n\n".join([
                f"Rule ID: {rule.rule_id}\nContent: {rule.content}"
                for rule in rules
            ])

            suggestions_created = []
            all_rule_ids = [rule.rule_id for rule in rules]

            for code_file in code_files:
                user_prompt = f"""Generate comprehensive test cases for the following code, ensuring all business rules are validated.

Business Rules:
{rules_context}

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please generate:
1. Unit tests mapped to Rule IDs
2. Integration test strategy
3. Regression test cases
4. Coverage analysis (what's missing)
5. Validation that business rules are enforced

Format your response as JSON:
{{
    "test_code": "complete test file code",
    "test_cases": [
        {{
            "test_name": "test name",
            "test_type": "unit/integration/regression",
            "rule_ids": ["BL-001"],
            "description": "what it tests"
        }}
    ],
    "coverage_analysis": {{
        "covered_rules": ["BL-001", "BL-002"],
        "missing_coverage": ["BL-003"],
        "coverage_percentage": 75
    }},
    "business_rule_validation": [
        {{
            "rule_id": "BL-001",
            "validated": true,
            "test_cases": ["test case 1", "test case 2"]
        }}
    ],
    "explanation": "test suite explanation"
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

                    test_data = json.loads(json_str)
                except (json.JSONDecodeError, KeyError):
                    test_data = {
                        "test_code": response,
                        "test_cases": [],
                        "coverage_analysis": {},
                        "explanation": "Generated unit tests"
                    }

                # Create suggestion
                suggestion = self.create_suggestion(
                    project_id=project_id,
                    content=json.dumps(test_data, indent=2),
                    code_file_id=code_file.id,
                    rule_id=all_rule_ids[0] if all_rule_ids else None
                )
                suggestions_created.append(suggestion.id)

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated tests for {len(suggestions_created)} file(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "rule_ids_processed": all_rule_ids,
                "message": f"Generated test cases mapped to {len(all_rule_ids)} business rule(s) for {len(suggestions_created)} file(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
