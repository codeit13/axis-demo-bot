"""Code Template Agent - Provides production-ready microservice templates."""
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class CodeTemplateAgent(BaseAgent):
    """Code Template Agent for generating microservice templates."""

    def get_agent_type(self) -> AgentType:
        return AgentType.CODE_TEMPLATE_AGENT

    def get_system_prompt(self) -> str:
        return """You are a Code Template Agent that provides production-ready microservice templates.
Your role is to:
1. Generate complete microservice boilerplate code
2. Include best practices and coding standards
3. Provide templates for different service types (REST API, gRPC, Event-driven, etc.)
4. Include testing frameworks and configurations
5. Follow Axis Bank coding standards
6. Provide complete project scaffolding

Always ensure:
- Templates are production-ready
- Code follows best practices
- Includes proper error handling
- Has comprehensive documentation
- Includes testing setup"""

    def analyze(
        self,
        project_id: int,
        template_type: Optional[str] = None,
        service_name: Optional[str] = None,
        technologies: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate code template or list available templates.

        Args:
            project_id: Project ID
            template_type: Type of template (rest_api, grpc, event_driven, etc.)
            service_name: Name of the service
            technologies: List of technologies to use
            **kwargs: Additional parameters

        Returns:
            Analysis result with template information
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            # If no template_type specified, return list of available templates
            if not template_type:
                templates = self._get_available_templates()
                return {
                    "status": "success",
                    "templates": templates,
                    "message": "Available templates retrieved"
                }

            # Generate specific template
            technologies = technologies or ["Python", "FastAPI", "PostgreSQL"]
            service_name = service_name or "Microservice"

            user_prompt = f"""Generate a complete production-ready microservice template.

Template Type: {template_type}
Service Name: {service_name}
Technologies: {', '.join(technologies)}

Please generate:
1. Complete project structure
2. Main service code with best practices
3. Configuration files
4. Testing setup
5. Docker configuration
6. README with setup instructions
7. API routes/endpoints (if applicable)
8. Database models (if applicable)
9. Error handling
10. Logging configuration

Format your response as JSON:
{{
    "template_type": "{template_type}",
    "service_name": "{service_name}",
    "technologies": {json.dumps(technologies)},
    "project_structure": {{
        "files": [
            {{"path": "path/to/file", "content": "file content", "description": "file description"}}
        ]
    }},
    "features": ["list of features"],
    "setup_instructions": "setup instructions",
    "dependencies": ["list of dependencies"]
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

                template_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError):
                template_data = {
                    "template_type": template_type,
                    "service_name": service_name,
                    "technologies": technologies,
                    "project_structure": {"files": []},
                    "features": [],
                    "setup_instructions": "See generated code",
                    "dependencies": []
                }

            # Create suggestion
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(template_data, indent=2)
            )

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated {template_type} template for {service_name}"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "template": template_data,
                "message": f"Generated {template_type} template"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}

    def _get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available templates."""
        return [
            {
                "id": "rest_api",
                "title": "REST API Microservice",
                "type": "REST API",
                "description": "Complete REST API microservice with FastAPI, PostgreSQL, and testing setup",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Pytest", "Docker"],
                "features": [
                    "RESTful API endpoints",
                    "Database models with SQLAlchemy",
                    "Unit and integration tests",
                    "Docker configuration",
                    "API documentation",
                    "Error handling",
                    "Logging"
                ]
            },
            {
                "id": "grpc",
                "title": "gRPC Microservice",
                "type": "gRPC",
                "description": "gRPC microservice template with protocol buffers and service definitions",
                "technologies": ["Python", "gRPC", "Protocol Buffers", "Pytest"],
                "features": [
                    "gRPC service definitions",
                    "Protocol buffer schemas",
                    "Service implementation",
                    "Client examples",
                    "Testing framework",
                    "Docker configuration"
                ]
            },
            {
                "id": "event_driven",
                "title": "Event-Driven Microservice",
                "type": "Event-Driven",
                "description": "Event-driven microservice with message queue integration",
                "technologies": ["Python", "FastAPI", "RabbitMQ", "Redis", "Docker"],
                "features": [
                    "Event producers and consumers",
                    "Message queue integration",
                    "Event handlers",
                    "Event schemas",
                    "Testing with mock queues",
                    "Docker configuration"
                ]
            },
            {
                "id": "graphql",
                "title": "GraphQL API Service",
                "type": "GraphQL",
                "description": "GraphQL API service with schema definitions and resolvers",
                "technologies": ["Python", "Graphene", "FastAPI", "PostgreSQL"],
                "features": [
                    "GraphQL schema definitions",
                    "Query and mutation resolvers",
                    "Type system",
                    "API documentation",
                    "Testing framework",
                    "Docker configuration"
                ]
            }
        ]
