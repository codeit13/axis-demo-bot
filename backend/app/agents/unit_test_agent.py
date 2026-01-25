"""Unit Test Agent - Generates unit tests for code."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class UnitTestAgent(BaseAgent):
    """Agent that generates unit tests for code files."""

    def get_agent_type(self) -> AgentType:
        return AgentType.UNIT_TEST

    def get_system_prompt(self) -> str:
        return """You are a senior software engineer specializing in writing comprehensive unit tests.
Your task is to analyze code and generate high-quality unit tests that cover:
- Normal cases
- Edge cases
- Error scenarios
- Boundary conditions

Always write tests that are clear, maintainable, and follow best practices.
Provide tests in the appropriate testing framework for the language (e.g., pytest for Python, Jest for JavaScript)."""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate unit tests for code.

        Args:
            project_id: Project ID
            code_file_id: Optional specific code file ID
            **kwargs: Additional parameters

        Returns:
            Analysis result with suggestions
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            # Get code files
            if code_file_id:
                code_file = self.get_code_file(code_file_id)
                if not code_file:
                    return {"error": "Code file not found", "status": "error"}
                code_files = [code_file]
            else:
                code_files = self.get_project_code_files(project_id)
                if not code_files:
                    return {"error": "No code files found in project", "status": "error"}

            suggestions_created = []
            for code_file in code_files:
                # Generate unit tests
                user_prompt = f"""Analyze the following code and generate comprehensive unit tests.

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please provide:
1. A complete test file with all necessary imports
2. Test cases covering normal cases, edge cases, and error scenarios
3. Brief explanation of what each test covers

Format your response as JSON with the following structure:
{{
    "test_code": "complete test file code",
    "test_cases": ["list of test case descriptions"],
    "explanation": "brief explanation of the test suite"
}}"""

                response = self.generate_with_groq(user_prompt, temperature=0.2)
                
                # Try to parse as JSON, fallback to text
                try:
                    if "```json" in response:
                        json_str = response.split("```json")[1].split("```")[0].strip()
                    elif "```" in response:
                        json_str = response.split("```")[1].split("```")[0].strip()
                    else:
                        json_str = response.strip()
                    
                    test_data = json.loads(json_str)
                    content = json.dumps(test_data, indent=2)
                except (json.JSONDecodeError, KeyError):
                    # Fallback: store as text
                    content = json.dumps({
                        "test_code": response,
                        "explanation": "Generated unit tests"
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
                result_summary=f"Generated unit tests for {len(suggestions_created)} file(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "message": f"Generated unit tests for {len(suggestions_created)} file(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
