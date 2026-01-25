"""Documentation Agent - Generates documentation from code."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class DocumentationAgent(BaseAgent):
    """Agent that generates documentation from code."""

    def get_agent_type(self) -> AgentType:
        return AgentType.DOCUMENTATION

    def get_system_prompt(self) -> str:
        return """You are a technical writer specializing in code documentation.
Your task is to generate comprehensive documentation including:
- API documentation
- Code comments and docstrings
- README files
- Function and class documentation
- Usage examples

Always write clear, concise, and helpful documentation that follows best practices for the language."""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        doc_type: str = "all",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate documentation.

        Args:
            project_id: Project ID
            code_file_id: Optional specific code file ID
            doc_type: Type of documentation ("api", "readme", "comments", "all")
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
                # Generate documentation based on type
                doc_instructions = {
                    "api": "Generate API documentation with endpoint descriptions, parameters, and examples.",
                    "readme": "Generate a comprehensive README file with project description, setup instructions, and usage examples.",
                    "comments": "Generate code comments and docstrings for all functions and classes.",
                    "all": "Generate all types of documentation: API docs, README, and code comments."
                }
                
                instruction = doc_instructions.get(doc_type, doc_instructions["all"])

                user_prompt = f"""Generate documentation for the following code.

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}
Documentation Type: {doc_type}

{instruction}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please provide:
1. Complete documentation based on the requested type
2. Clear explanations and examples
3. Proper formatting for the documentation type

Format your response as JSON:
{{
    "documentation": "complete documentation content",
    "doc_type": "{doc_type}",
    "sections": ["list of documentation sections"],
    "examples": ["usage examples if applicable"]
}}"""

                response = self.generate_with_groq(user_prompt, temperature=0.2)
                
                # Try to parse as JSON
                try:
                    if "```json" in response:
                        json_str = response.split("```json")[1].split("```")[0].strip()
                    elif "```" in response:
                        json_str = response.split("```")[1].split("```")[0].strip()
                    else:
                        json_str = response.strip()
                    
                    doc_data = json.loads(json_str)
                    content = json.dumps(doc_data, indent=2)
                except (json.JSONDecodeError, KeyError):
                    # Fallback: store as text
                    content = json.dumps({
                        "documentation": response,
                        "doc_type": doc_type,
                        "explanation": "Generated documentation"
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
                result_summary=f"Generated {doc_type} documentation for {len(suggestions_created)} file(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "message": f"Generated documentation for {len(suggestions_created)} file(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
