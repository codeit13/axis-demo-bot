"""Code Review Agent - Reviews code and suggests improvements."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class CodeReviewAgent(BaseAgent):
    """Agent that reviews code and suggests improvements."""

    def get_agent_type(self) -> AgentType:
        return AgentType.CODE_REVIEW

    def get_system_prompt(self) -> str:
        return """You are a senior code reviewer with expertise in code quality, best practices, and software engineering principles.
Your task is to review code and provide constructive feedback on:
- Code quality and readability
- Best practices and design patterns
- Performance optimizations
- Security considerations
- Maintainability and scalability
- Documentation and comments

Always provide actionable, specific feedback with examples."""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Review code and generate suggestions.

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
                # Generate code review
                user_prompt = f"""Review the following code and provide comprehensive feedback.

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please provide a code review covering:
1. Code quality and readability
2. Best practices and design patterns
3. Performance considerations
4. Security issues
5. Maintainability concerns
6. Suggestions for improvements with code examples

Format your response as JSON:
{{
    "overall_rating": "excellent/good/needs_improvement",
    "strengths": ["list of strengths"],
    "issues": [
        {{
            "type": "quality/performance/security/etc",
            "severity": "high/medium/low",
            "description": "issue description",
            "suggestion": "improvement suggestion",
            "code_example": "improved code example (if applicable)"
        }}
    ],
    "recommendations": ["list of recommendations"],
    "summary": "overall review summary"
}}"""

                response = self.generate_with_groq(user_prompt, temperature=0.3)
                
                # Parse response using robust JSON extractor
                from ..utils.json_extractor import extract_json_from_text
                
                extracted = extract_json_from_text(response, fallback_to_text=False)
                
                if isinstance(extracted, dict):
                    content = json.dumps(extracted, indent=2)
                else:
                    # Fallback: store as text
                    content = json.dumps({
                        "review": response,
                        "summary": "Generated code review"
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
                result_summary=f"Reviewed {len(suggestions_created)} file(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "message": f"Code review completed for {len(suggestions_created)} file(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
