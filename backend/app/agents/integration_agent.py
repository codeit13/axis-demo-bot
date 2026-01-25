"""Integration Agent - Generates API specifications from service descriptions."""
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class IntegrationAgent(BaseAgent):
    """Integration Agent for generating API specifications."""

    def get_agent_type(self) -> AgentType:
        return AgentType.INTEGRATION_AGENT

    def get_system_prompt(self) -> str:
        return """You are an Integration Agent that generates comprehensive API specifications in OpenAPI 3.0 format.
Your role is to:
1. Generate complete OpenAPI 3.0 specifications from service descriptions
2. Define all endpoints with request/response schemas
3. Include security requirements (OAuth 2.0, rate limiting, HTTPS)
4. Provide authentication and authorization details
5. Ensure OpenAPI 3.0 compliance
6. Generate production-ready API documentation

Always ensure:
- Specifications follow OpenAPI 3.0 standards
- All endpoints have proper schemas
- Security requirements are clearly defined
- Documentation is comprehensive and ready for frontend teams"""

    def analyze(
        self,
        project_id: int,
        service_name: Optional[str] = None,
        base_url: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate API specification from service description.

        Args:
            project_id: Project ID
            service_name: Service name
            base_url: Base URL for the API
            description: Service description
            **kwargs: Additional parameters

        Returns:
            Analysis result with API specification
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            if not service_name and not description:
                return {"error": "Service name or description is required", "status": "error"}

            # Default values
            service_name = service_name or "API Service"
            base_url = base_url or "https://api.example.com/v1"
            description = description or "API service"

            user_prompt = f"""Generate a complete OpenAPI 3.0 specification for the following service. The specification MUST be fully compatible with Swagger Editor and follow OpenAPI 3.0.0 standards exactly.

Service Name: {service_name}
Base URL: {base_url}
Description: {description}

CRITICAL REQUIREMENTS:
1. The OpenAPI spec MUST be valid YAML that can be directly pasted into Swagger Editor (https://editor.swagger.io/)
2. Follow OpenAPI 3.0.0 specification strictly
3. Include complete schemas for all request/response bodies
4. Define all components in the components/schemas section
5. Use proper YAML formatting (2 spaces indentation, no tabs)
6. Include security schemes in components/securitySchemes
7. All endpoints must have proper tags, summaries, and descriptions
8. Include examples for all request/response bodies
9. Define proper error responses (400, 401, 403, 404, 500, etc.)
10. Use proper data types (string, integer, number, boolean, array, object)

Please generate:
1. Complete OpenAPI 3.0.0 specification in YAML format (ready for Swagger Editor)
2. All relevant endpoints with HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.)
3. Complete request/response schemas with examples
4. Security schemes (OAuth 2.0, API Key, etc.) in components/securitySchemes
5. Reusable schemas in components/schemas
6. Proper error response schemas
7. Tags for organizing endpoints
8. Server information

The openapi_spec field MUST contain valid YAML that can be directly copied and pasted into Swagger Editor (https://editor.swagger.io/) without any modifications.

EXAMPLE of valid OpenAPI 3.0.0 YAML structure:
openapi: 3.0.0
info:
  title: Service Name
  version: 1.0.0
  description: Service description
servers:
  - url: https://api.example.com/v1
    description: Production server
paths:
  /endpoint:
    get:
      summary: Endpoint summary
      description: Endpoint description
      tags:
        - tag-name
      security:
        - OAuth2: []
      parameters:
        - name: param
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseModel'
        '400':
          $ref: '#/components/responses/BadRequest'
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read: Read access
            write: Write access
  schemas:
    ResponseModel:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string

Format your response as JSON:
{{
    "openapi_spec": "complete OpenAPI 3.0.0 YAML specification (ready for Swagger Editor - must be valid YAML)",
    "serviceName": "{service_name}",
    "version": "1.0.0",
    "baseUrl": "{base_url}",
    "description": "{description}",
    "authentication": "OAuth 2.0",
    "endpoints": [
        {{
            "path": "/api/endpoint",
            "method": "GET",
            "summary": "Endpoint summary",
            "description": "Endpoint description",
            "parameters": [],
            "responses": {{
                "200": {{
                    "description": "Success response",
                    "schema": {{}}
                }}
            }}
        }}
    ],
    "securityRequirements": [
        "OAuth 2.0 authentication required",
        "Rate limiting: 100 requests per minute",
        "All requests must be sent over HTTPS"
    ]
}}"""

            response = self.generate_with_groq(user_prompt, temperature=0.2)

            # Parse response
            try:
                # Try to extract JSON from markdown code blocks
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    # Could be YAML or JSON in code block
                    parts = response.split("```")
                    if len(parts) >= 3:
                        json_str = parts[1].strip()
                        # If it looks like YAML, try to find JSON part
                        if json_str.startswith("yaml") or json_str.startswith("openapi"):
                            # Look for JSON part
                            if "{" in response:
                                json_start = response.find("{")
                                json_end = response.rfind("}") + 1
                                json_str = response[json_start:json_end]
                    else:
                        json_str = response.strip()
                else:
                    json_str = response.strip()
                
                # If response contains YAML directly, extract it
                if "openapi:" in response and "```" not in response:
                    # Response might be pure YAML, wrap it in JSON
                    yaml_start = response.find("openapi:")
                    yaml_content = response[yaml_start:].strip()
                    spec_data = {
                        "openapi_spec": yaml_content,
                        "serviceName": service_name,
                        "version": "1.0.0",
                        "baseUrl": base_url,
                        "description": description,
                        "authentication": "OAuth 2.0",
                        "endpoints": [],
                        "securityRequirements": [
                            "OAuth 2.0 authentication required",
                            "Rate limiting: 100 requests per minute",
                            "All requests must be sent over HTTPS"
                        ]
                    }
                else:
                    spec_data = json.loads(json_str)
            except (json.JSONDecodeError, KeyError) as e:
                # Fallback: create basic structure
                spec_data = {
                    "openapi_spec": response if "openapi" in response.lower() else f"""openapi: 3.0.0
info:
  title: {service_name}
  version: 1.0.0
  description: {description}
servers:
  - url: {base_url}
paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
""",
                    "serviceName": service_name,
                    "version": "1.0.0",
                    "baseUrl": base_url,
                    "description": description,
                    "authentication": "OAuth 2.0",
                    "endpoints": [],
                    "securityRequirements": [
                        "OAuth 2.0 authentication required",
                        "Rate limiting: 100 requests per minute",
                        "All requests must be sent over HTTPS"
                    ]
                }

            # Create suggestion
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(spec_data, indent=2)
            )

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary=f"Generated API specification for {service_name}"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "spec": spec_data,
                "message": f"Generated API specification for {service_name}"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
