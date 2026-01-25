"""API Spec Agent - Generates API specifications from code."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class APISpecAgent(BaseAgent):
    """Agent that generates API specifications and OpenAPI/Swagger docs."""

    def get_agent_type(self) -> AgentType:
        return AgentType.API_SPEC

    def get_system_prompt(self) -> str:
        return """You are an API design expert specializing in OpenAPI/Swagger specifications.
Your task is to analyze code (especially API endpoints, routes, and handlers) and generate:
- Complete OpenAPI 3.0 specifications
- Request/response schemas
- Parameter definitions
- Example requests and responses
- API endpoint signatures

Always follow OpenAPI 3.0 standards and provide clear, comprehensive documentation."""

    def analyze(
        self,
        project_id: int,
        code_file_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate API specifications.

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
                # Generate API spec
                user_prompt = f"""Analyze the following code and generate a complete OpenAPI 3.0 specification.

Code File: {code_file.file_path}
Language: {code_file.language or 'Unknown'}

Code:
```{code_file.language or ''}
{code_file.content}
```

Please provide:
1. Complete OpenAPI 3.0 specification in YAML format
2. All endpoints with request/response schemas
3. Parameter definitions
4. Example requests and responses

Format your response as JSON with the following structure:
{{
    "openapi_spec": "complete OpenAPI YAML specification",
    "endpoints": ["list of endpoint summaries"],
    "schemas": ["list of schema definitions"],
    "explanation": "brief explanation of the API"
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
                    
                    spec_data = json.loads(json_str)
                    content = json.dumps(spec_data, indent=2)
                except (json.JSONDecodeError, KeyError):
                    # Fallback: store as text
                    content = json.dumps({
                        "openapi_spec": response,
                        "explanation": "Generated API specification"
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
                result_summary=f"Generated API specs for {len(suggestions_created)} file(s)"
            )

            return {
                "status": "success",
                "suggestions_created": suggestions_created,
                "message": f"Generated API specifications for {len(suggestions_created)} file(s)"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
