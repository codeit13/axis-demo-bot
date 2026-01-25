"""Business Logic & Policy Agent - Canonical source for business rules."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, BusinessRule, RuleStatus
from ..services.groq_service import GroqService
from ..services.rule_service import RuleService


class BusinessLogicAgent(BaseAgent):
    """Agent 1: Business Logic & Policy Agent (Canonical)."""

    def get_agent_type(self) -> AgentType:
        return AgentType.BUSINESS_LOGIC_POLICY

    def get_system_prompt(self) -> str:
        return """You are a Business Logic & Policy Agent, the canonical source for business rules.
Your role is to:
1. Ingest and structure business logic from leadership
2. Detect ambiguities, conflicting rules, and missing edge cases
3. Ask clarifying questions when needed
4. Maintain versioned business rules with explicit assumptions
5. Generate Rule IDs (BL-001, BL-002, etc.)
6. Create decision logs

Always ensure rules are:
- Clear and unambiguous
- Traceable to business decisions
- Versioned properly
- Free of conflicts with existing rules

When you detect conflicts or ambiguities, clearly state them and ask for clarification."""

    def analyze(
        self,
        project_id: int,
        business_logic_text: Optional[str] = None,
        rule_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze business logic and create/update business rules.

        Args:
            project_id: Project ID
            business_logic_text: Business logic description/requirements
            rule_id: Optional existing Rule ID to update
            **kwargs: Additional parameters

        Returns:
            Analysis result with rule creation/update
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            # Validate business logic text is provided for new rules
            if not rule_id and not business_logic_text:
                return {
                    "error": "Business logic description is required. Please provide a description of your business logic, requirements, and policies.",
                    "status": "error"
                }

            groq_service = GroqService()

            # If updating existing rule
            if rule_id:
                existing_rule = RuleService.get_rule_by_id(self.db, rule_id)
                if not existing_rule:
                    return {"error": f"Rule {rule_id} not found", "status": "error"}

                user_prompt = f"""Update the following business rule based on new requirements.

Existing Rule:
Rule ID: {existing_rule.rule_id}
Version: {existing_rule.version}
Content: {existing_rule.content}

New Requirements:
{business_logic_text or 'No new requirements provided'}

Please:
1. Analyze the changes
2. Detect any conflicts with other rules
3. Identify ambiguities
4. Generate updated rule content
5. Create a diff showing what changed
6. Suggest questions for clarification if needed

Format your response as JSON:
{{
    "updated_content": "updated business rule content",
    "diff": "what changed from previous version",
    "conflicts_detected": ["list of potential conflicts"],
    "ambiguities": ["list of ambiguities"],
    "clarifying_questions": ["questions that need answers"],
    "assumptions": ["explicit assumptions made"]
}}"""
            else:
                # Creating new rules
                user_prompt = f"""Analyze the following business logic and extract ALL individual business rules.

Business Logic Description:
{business_logic_text or 'No business logic provided'}

Please:
1. Extract EACH distinct business rule as a separate item
2. Each rule should be clear, unambiguous, and standalone
3. Identify any ambiguities or missing information
4. Detect potential conflicts between rules
5. List explicit assumptions for each rule
6. Suggest clarifying questions if needed

IMPORTANT: Return an array of rules, where each rule is a separate entity.

Format your response as JSON:
{{
    "rules": [
        {{
            "rule_id": "BL-XXX (you will suggest, but we will assign actual IDs)",
            "content": "Single, clear business rule statement",
            "assumptions": ["assumptions for this specific rule"],
            "edge_cases": ["edge cases for this rule"]
        }}
    ],
    "conflicts_detected": ["list of potential conflicts between rules"],
    "ambiguities": ["list of ambiguities"],
    "clarifying_questions": ["questions that need answers"],
    "overall_assumptions": ["assumptions that apply to all rules"]
}}"""

            response = groq_service.generate(
                system_prompt=self.get_system_prompt(),
                user_prompt=user_prompt,
                temperature=0.2
            )

            # Parse response using robust JSON extractor
            from ..utils.json_extractor import extract_json_from_text
            
            extracted = extract_json_from_text(response, fallback_to_text=False)
            
            if isinstance(extracted, dict):
                analysis_data = extracted
            else:
                # Fallback: create structure with response as content
                analysis_data = {
                    "rule_content" if not rule_id else "updated_content": response,
                    "conflicts_detected": [],
                    "ambiguities": [],
                    "clarifying_questions": [],
                    "assumptions": []
                }

            # Extract individual rules from response
            rules_list = analysis_data.get("rules", [])
            if not rules_list and "rule_content" in analysis_data:
                # Fallback: try to parse multiple rules from rule_content if they're listed with IDs
                rule_content = analysis_data.get("rule_content", "")
                if isinstance(rule_content, str):
                    # Try to extract individual rules if they're formatted as "BL-XXX: rule text"
                    import re
                    rule_pattern = r'(BL-\d+):\s*([^\n]+(?:\n(?!BL-\d+:)[^\n]+)*)'
                    matches = re.findall(rule_pattern, rule_content, re.MULTILINE)
                    if matches:
                        # Found multiple rules with IDs
                        rules_list = [{
                            "content": content.strip(),
                            "assumptions": analysis_data.get("assumptions", []),
                            "edge_cases": analysis_data.get("edge_cases", [])
                        } for rule_id, content in matches]
                    else:
                        # Single rule or no ID pattern found
                        rules_list = [{
                            "content": rule_content,
                            "assumptions": analysis_data.get("assumptions", []),
                            "edge_cases": analysis_data.get("edge_cases", [])
                        }]
                else:
                    # rule_content is not a string
                    rules_list = [{
                        "content": str(analysis_data.get("rule_content", "")),
                        "assumptions": analysis_data.get("assumptions", []),
                        "edge_cases": analysis_data.get("edge_cases", [])
                    }]

            # Create multiple business rules if we have a list
            created_rule_ids = []
            if not rule_id and rules_list:
                for rule_data in rules_list:
                    rule_content = rule_data.get("content", "")
                    if not rule_content:
                        continue
                    
                    # Ensure rule_content is a string
                    if isinstance(rule_content, dict):
                        rule_content = json.dumps(rule_content, indent=2)
                    elif not isinstance(rule_content, str):
                        rule_content = str(rule_content) if rule_content else ""
                    
                    # Check for conflicts
                    conflicts = RuleService.detect_conflicts(self.db, project_id, rule_content)
                    if conflicts:
                        analysis_data["conflicts_detected"].extend([c["rule_id"] for c in conflicts])
                    
                    # Generate unique rule ID
                    new_rule_id = RuleService.generate_rule_id(self.db, project_id)
                    
                    # Get assumptions for this specific rule or use overall assumptions
                    rule_assumptions = rule_data.get("assumptions", [])
                    if not rule_assumptions:
                        rule_assumptions = analysis_data.get("overall_assumptions", [])
                    
                    # Create business rule
                    business_rule = BusinessRule(
                        rule_id=new_rule_id,
                        project_id=project_id,
                        version="1.0.0",
                        content=rule_content,
                        status=RuleStatus.PENDING_APPROVAL,
                        assumptions=json.dumps(rule_assumptions),
                        created_by=kwargs.get("created_by", "system")
                    )
                    self.db.add(business_rule)
                    created_rule_ids.append(new_rule_id)
                
                self.db.commit()
                
                # Refresh all created rules
                for rule_id in created_rule_ids:
                    rule = RuleService.get_rule_by_id(self.db, rule_id)
                    if rule:
                        self.db.refresh(rule)

            # Create or update business rule (for updates)
            if rule_id:
                # Update existing rule
                existing_rule.content = analysis_data.get("updated_content", existing_rule.content)
                existing_rule.assumptions = json.dumps(analysis_data.get("assumptions", []))
                existing_rule.status = RuleStatus.PENDING_APPROVAL
                self.db.commit()
                self.db.refresh(existing_rule)

                # Create version
                RuleService.create_rule_version(
                    db=self.db,
                    rule=existing_rule,
                    new_content=existing_rule.content,
                    created_by=kwargs.get("created_by", "system"),
                    diff=analysis_data.get("diff", "")
                )

                rule_id_result = existing_rule.rule_id
                
                # Create suggestion for update
                suggestion_content = json.dumps(analysis_data, indent=2)
                suggestion = self.create_suggestion(
                    project_id=project_id,
                    content=suggestion_content,
                    rule_id=rule_id_result
                )

                self.log_agent_run(
                    project_id=project_id,
                    status="success",
                    result_summary=f"Updated business rule {rule_id_result}"
                )

                return {
                    "status": "success",
                    "rule_id": rule_id_result,
                    "suggestion_id": suggestion.id,
                    "conflicts_detected": analysis_data.get("conflicts_detected", []),
                    "ambiguities": analysis_data.get("ambiguities", []),
                    "clarifying_questions": analysis_data.get("clarifying_questions", []),
                    "message": f"Business rule {rule_id_result} updated. Human approval required."
                }
            else:
                # Multiple rules were created above
                if created_rule_ids:
                    # Create suggestion with all rules info
                    suggestion_content = json.dumps(analysis_data, indent=2)
                    suggestion = self.create_suggestion(
                        project_id=project_id,
                        content=suggestion_content,
                        rule_id=created_rule_ids[0]  # Link to first rule
                    )

                    self.log_agent_run(
                        project_id=project_id,
                        status="success",
                        result_summary=f"Created {len(created_rule_ids)} business rules: {', '.join(created_rule_ids)}"
                    )

                    return {
                        "status": "success",
                        "rule_ids": created_rule_ids,
                        "suggestion_id": suggestion.id,
                        "conflicts_detected": analysis_data.get("conflicts_detected", []),
                        "ambiguities": analysis_data.get("ambiguities", []),
                        "clarifying_questions": analysis_data.get("clarifying_questions", []),
                        "message": f"Created {len(created_rule_ids)} business rules. Human approval required for each."
                    }
                else:
                    return {
                        "status": "error",
                        "error": "No rules were extracted from the business logic description."
                    }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
