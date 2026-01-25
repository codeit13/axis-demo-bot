"""Bug Scanner Agent - Scans for bugs and suggests fixes."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType, Issue
from ..services.bitbucket_mock import BitbucketMockService


class BugScannerAgent(BaseAgent):
    """Agent that scans for bugs and suggests fixes."""

    def get_agent_type(self) -> AgentType:
        return AgentType.BUG_SCANNER

    def get_system_prompt(self) -> str:
        return """You are a senior software engineer and bug hunter with expertise in identifying and fixing bugs.
Your task is to:
- Analyze code for potential bugs, vulnerabilities, and issues
- Suggest fixes for identified bugs
- Review bug reports and provide detailed fix suggestions
- Consider edge cases, error handling, and best practices

Always provide clear explanations of bugs and comprehensive fix suggestions with code examples."""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        issue_id: Optional[int] = None,
        scan_all: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Scan for bugs and suggest fixes.

        Args:
            project_id: Project ID
            code_file_id: Optional specific code file ID
            issue_id: Optional issue ID (human-identified bug)
            scan_all: If True, scan all files in project
            **kwargs: Additional parameters

        Returns:
            Analysis result with suggestions
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            suggestions_created = []
            issues_created = []

            # Handle human-identified bug (issue_id provided)
            if issue_id:
                issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
                if not issue:
                    return {"error": "Issue not found", "status": "error"}

                # Get related code file if available
                code_file = None
                if issue.project.code_files:
                    code_file = issue.project.code_files[0]  # Use first file or find by context

                # Generate fix suggestion
                user_prompt = f"""A bug has been identified in the project. Please analyze and suggest a fix.

Bug Report:
Title: {issue.title}
Description: {issue.description}

"""
                if code_file:
                    user_prompt += f"""Related Code File: {code_file.file_path}

Code:
```{code_file.language or ''}
{code_file.content}
```

"""
                user_prompt += """Please provide:
1. Detailed explanation of the bug
2. Root cause analysis
3. Suggested fix with corrected code
4. Unit tests to prevent regression
5. Brief PR description

Format your response as JSON:
{{
    "bug_explanation": "detailed explanation",
    "root_cause": "root cause analysis",
    "suggested_fix": "corrected code",
    "unit_tests": "unit tests for the fix",
    "pr_description": "PR description"
}}"""

                response = self.generate_with_groq(user_prompt, temperature=0.2)
                
                # Parse response using robust JSON extractor
                from ..utils.json_extractor import extract_json_from_text
                
                extracted = extract_json_from_text(response, fallback_to_text=False)
                
                if isinstance(extracted, dict):
                    content = json.dumps(extracted, indent=2)
                else:
                    # Fallback: create structure with response
                    content = json.dumps({
                        "bug_explanation": response,
                        "suggested_fix": "See explanation above"
                    }, indent=2)

                suggestion = self.create_suggestion(
                    project_id=project_id,
                    content=content,
                    code_file_id=code_file.id if code_file else None,
                    issue_id=issue_id
                )
                suggestions_created.append(suggestion.id)

            # Scan codebase for bugs (if scan_all or no issue_id)
            if scan_all or not issue_id:
                code_files = self.get_project_code_files(project_id)
                if code_files:
                    for code_file in code_files:
                        user_prompt = f"""Scan the following code for potential bugs, vulnerabilities, and issues.

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please identify:
1. Potential bugs or logical errors
2. Security vulnerabilities
3. Performance issues
4. Edge cases not handled
5. Best practice violations

For each issue found, provide:
- Issue description
- Severity (high/medium/low)
- Suggested fix

Format your response as JSON:
{{
    "issues_found": [
        {{
            "description": "issue description",
            "severity": "high/medium/low",
            "suggested_fix": "fix code or explanation"
        }}
    ],
    "summary": "overall summary"
}}"""

                        response = self.generate_with_groq(user_prompt, temperature=0.2)
                        
                        try:
                            if "```json" in response:
                                json_str = response.split("```json")[1].split("```")[0].strip()
                            elif "```" in response:
                                json_str = response.split("```")[1].split("```")[0].strip()
                            else:
                                json_str = response.strip()
                            
                            scan_data = json.loads(json_str)
                            
                            # Create Bitbucket issues for found bugs
                            if scan_data.get("issues_found"):
                                for bug in scan_data["issues_found"]:
                                    if bug.get("severity") in ["high", "medium"]:
                                        issue_result = BitbucketMockService.create_issue(
                                            db=self.db,
                                            project_id=project_id,
                                            title=f"Potential Bug: {bug.get('description', 'Unknown')[:100]}",
                                            description=f"Severity: {bug.get('severity', 'unknown')}\n\n{bug.get('description', '')}\n\nSuggested Fix:\n{bug.get('suggested_fix', '')}",
                                            code_file_id=code_file.id
                                        )
                                        issues_created.append(issue_result["bitbucket_issue_id"])

                            content = json.dumps(scan_data, indent=2)
                        except (json.JSONDecodeError, KeyError):
                            content = json.dumps({
                                "issues_found": [],
                                "summary": response
                            }, indent=2)

                        suggestion = self.create_suggestion(
                            project_id=project_id,
                            content=content,
                            code_file_id=code_file.id
                        )
                        suggestions_created.append(suggestion.id)

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Scanned for bugs, created {len(suggestions_created)} suggestion(s), {len(issues_created)} issue(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "issues_created": issues_created,
                "message": f"Bug scan completed. Created {len(suggestions_created)} suggestion(s) and {len(issues_created)} issue(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
