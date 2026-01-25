"""Prompt Amplifier Agent - Enhances developer prompts with context and best practices."""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..tables import AgentType


class PromptAmplifierAgent(BaseAgent):
    """Prompt Amplifier Agent for enhancing developer prompts."""

    def __init__(self, db: Session):
        """Initialize agent and load knowledge sources config."""
        super().__init__(db)
        self.knowledge_sources_config = self._load_knowledge_sources_config()

    def _load_knowledge_sources_config(self) -> Dict[str, Any]:
        """Load knowledge sources configuration from JSON file."""
        try:
            config_path = Path(__file__).parent.parent / "config" / "knowledge_sources.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Fallback to default config if file doesn't exist
                return self._get_default_config()
        except Exception as e:
            print(f"Warning: Failed to load knowledge sources config: {e}. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default knowledge sources configuration."""
        return {
            "knowledge_sources": [
                {
                    "name": "Security & Compliance Policies",
                    "type": "security_policies",
                    "description": "Security best practices and compliance requirements",
                    "priority": 10,
                    "instructions": "- Add authentication and authorization requirements\n- Include input validation and sanitization requirements\n- Specify encryption requirements for sensitive data\n- Add security headers and CORS policies\n- Include rate limiting and DDoS protection considerations\n- Specify secure communication protocols (HTTPS, TLS)\n- Add security logging and monitoring requirements"
                },
                {
                    "name": "Axis Bank Architecture Standards",
                    "type": "architecture_standards",
                    "description": "Internal naming conventions and architecture guidelines",
                    "priority": 10,
                    "instructions": "- Use camelCase for variables and functions\n- Use PascalCase for classes and components\n- Use UPPER_SNAKE_CASE for constants\n- Prefix API endpoints with /api/v{version}/\n- Use descriptive, business-domain specific names\n- Follow microservice naming patterns (e.g., payment-service, user-service)\n- Include proper namespace and package organization"
                },
                {
                    "name": "Best Practices Repository",
                    "type": "best_practices",
                    "description": "Performance optimization patterns and strategies",
                    "priority": 8,
                    "instructions": "- Add caching strategies (Redis, in-memory caching)\n- Include database query optimization requirements\n- Specify pagination for list endpoints\n- Add connection pooling requirements\n- Include async/await patterns where applicable\n- Specify timeout and retry policies\n- Add performance monitoring and metrics requirements\n- Include load balancing considerations"
                },
                {
                    "name": "Testing Standards",
                    "type": "testing_requirements",
                    "description": "Testing standards and coverage requirements",
                    "priority": 8,
                    "instructions": "- Require unit tests with >80% code coverage\n- Include integration test requirements\n- Specify test data setup and teardown\n- Add mocking and stubbing requirements\n- Include performance and load testing\n- Specify test automation in CI/CD pipeline\n- Add test documentation requirements"
                },
                {
                    "name": "Internal Microservice Templates",
                    "type": "design_patterns",
                    "description": "Internal design patterns and microservice templates",
                    "priority": 9,
                    "instructions": "- Use repository pattern for data access\n- Implement service layer pattern\n- Follow dependency injection principles\n- Use factory pattern for object creation\n- Implement observer pattern for event handling\n- Follow SOLID principles\n- Use design patterns from Axis Bank architecture standards"
                },
                {
                    "name": "AI Best Practices",
                    "type": "ai_knowledge",
                    "description": "General AI coding best practices and patterns",
                    "priority": 5,
                    "instructions": "- Follow clean code principles\n- Write self-documenting code\n- Include comprehensive error handling\n- Add proper logging and monitoring\n- Ensure code is testable and maintainable\n- Follow industry-standard coding conventions"
                }
            ],
            "rule_mapping": {
                "Always add security requirements": "security_policies",
                "Include Axis Bank naming conventions": "architecture_standards",
                "Suggest performance optimization": "best_practices",
                "Add testing requirements (>80% coverage)": "best_practices",
                "Reference internal design patterns": "design_patterns"
            }
        }

    def get_agent_type(self) -> AgentType:
        return AgentType.PROMPT_AMPLIFIER_AGENT

    def get_system_prompt(self) -> str:
        return """You are a Prompt Amplifier Agent that enhances developer prompts with context and best practices.
Your role is to:
1. Analyze developer prompts and identify missing context
2. Add technical requirements and best practices
3. Include relevant coding standards
4. Suggest clearer technical requirements
5. Add missing edge cases and error handling
6. Enhance prompts to generate better code

Always ensure:
- Enhanced prompts are clear and specific
- Include all necessary context
- Follow best practices and coding standards
- Add missing technical details
- Suggest improvements for better outcomes"""

    def _get_enhancement_rule_instructions(self, rule_text: str) -> str:
        """Get specific instructions for each enhancement rule from config or fallback to defaults."""
        # Try to get instructions from config file first
        rule_mapping = self.knowledge_sources_config.get("rule_mapping", {})
        knowledge_sources_list = self.knowledge_sources_config.get("knowledge_sources", [])
        
        # Map rule to source type
        source_type = rule_mapping.get(rule_text)
        
        if source_type:
            # Find knowledge source(s) of this type
            matching_sources = [s for s in knowledge_sources_list if s.get("type") == source_type]
            if matching_sources:
                # Use the highest priority source
                source = sorted(matching_sources, key=lambda x: x.get("priority", 0), reverse=True)[0]
                instructions = source.get("instructions")
                if instructions:
                    return instructions
        
        # Fallback to hardcoded instructions if not found in config
        rule_instructions = {
            "Always add security requirements": """
- Add authentication and authorization requirements
- Include input validation and sanitization requirements
- Specify encryption requirements for sensitive data
- Add security headers and CORS policies
- Include rate limiting and DDoS protection considerations
- Specify secure communication protocols (HTTPS, TLS)
- Add security logging and monitoring requirements""",
            
            "Include Axis Bank naming conventions": """
- Use camelCase for variables and functions
- Use PascalCase for classes and components
- Use UPPER_SNAKE_CASE for constants
- Prefix API endpoints with /api/v{version}/
- Use descriptive, business-domain specific names
- Follow microservice naming patterns (e.g., payment-service, user-service)
- Include proper namespace and package organization""",
            
            "Suggest performance optimization": """
- Add caching strategies (Redis, in-memory caching)
- Include database query optimization requirements
- Specify pagination for list endpoints
- Add connection pooling requirements
- Include async/await patterns where applicable
- Specify timeout and retry policies
- Add performance monitoring and metrics requirements
- Include load balancing considerations""",
            
            "Add testing requirements (>80% coverage)": """
- Require unit tests with >80% code coverage
- Include integration test requirements
- Specify test data setup and teardown
- Add mocking and stubbing requirements
- Include performance and load testing
- Specify test automation in CI/CD pipeline
- Add test documentation requirements""",
            
            "Reference internal design patterns": """
- Use repository pattern for data access
- Implement service layer pattern
- Follow dependency injection principles
- Use factory pattern for object creation
- Implement observer pattern for event handling
- Follow SOLID principles
- Use design patterns from Axis Bank architecture standards"""
        }
        return rule_instructions.get(rule_text, f"- Apply best practices for: {rule_text}")

    def analyze(
        self,
        project_id: int,
        original_prompt: Optional[str] = None,
        context: Optional[str] = None,
        agent_config: Optional[Dict[str, Any]] = None,
        enhancement_rules: Optional[list] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Enhance a developer prompt.

        Args:
            project_id: Project ID
            original_prompt: Original prompt from developer
            context: Additional context (codebase, requirements, etc.)
            agent_config: Agent configuration (temperature, max_tokens, etc.)
            **kwargs: Additional parameters

        Returns:
            Analysis result with enhanced prompt
        """
        try:
            project = self.get_project(project_id)
            if not project:
                return {"error": "Project not found", "status": "error"}

            if not original_prompt:
                return {"error": "Original prompt is required", "status": "error"}

            # Track knowledge sources used
            knowledge_sources_used = []
            
            # Get project context
            code_files = self.get_project_code_files(project_id)
            code_context = ""
            if code_files:
                code_context = "\n\nExisting Codebase Context:\n"
                for cf in code_files[:5]:  # Limit to first 5 files
                    code_context += f"\nFile: {cf.file_path}\n```{cf.language or ''}\n{cf.content[:300]}...\n```"
                knowledge_sources_used.append({
                    "source": "Project Codebase",
                    "type": "codebase",
                    "description": f"Analyzed {len(code_files)} code files from project",
                    "files_analyzed": len(code_files)
                })

            additional_context = context or ""
            if additional_context:
                code_context += f"\n\nAdditional Context:\n{additional_context}"
                knowledge_sources_used.append({
                    "source": "User Provided Context",
                    "type": "user_context",
                    "description": "Additional context provided by user"
                })

            # Process enhancement rules
            enhancement_rules = enhancement_rules or []
            enabled_rules = [rule for rule in enhancement_rules if rule.get('enabled', False)]
            
            enhancement_instructions = ""
            if enabled_rules:
                enhancement_instructions = "\n\nApply the following enhancement rules:\n"
                for rule in enabled_rules:
                    rule_text = rule.get('text', '')
                    instructions = self._get_enhancement_rule_instructions(rule_text)
                    enhancement_instructions += f"\n{rule_text}:\n{instructions}\n"
                
                # Track which knowledge bases were used based on rules
                # Load from config file
                rule_mapping = self.knowledge_sources_config.get("rule_mapping", {})
                knowledge_sources_list = self.knowledge_sources_config.get("knowledge_sources", [])
                
                # Create a lookup dictionary by type for faster access
                sources_by_type = {}
                for source in knowledge_sources_list:
                    source_type = source.get("type")
                    if source_type not in sources_by_type:
                        sources_by_type[source_type] = []
                    sources_by_type[source_type].append(source)
                
                # Map enabled rules to knowledge sources
                for rule in enabled_rules:
                    rule_text = rule.get('text', '')
                    source_type = rule_mapping.get(rule_text)
                    
                    if source_type and source_type in sources_by_type:
                        # Get all sources of this type (sorted by priority)
                        sources = sorted(
                            sources_by_type[source_type],
                            key=lambda x: x.get("priority", 0),
                            reverse=True
                        )
                        
                        # Add each source (avoid duplicates)
                        for source in sources:
                            source_info = {
                                "source": source.get("name"),
                                "type": source.get("type"),
                                "description": source.get("description")
                            }
                            if not any(ks["source"] == source_info["source"] for ks in knowledge_sources_used):
                                knowledge_sources_used.append(source_info)
            
            # Add general AI knowledge source (always included)
            # Check if it's already in the config, otherwise add default
            ai_knowledge_sources = [s for s in knowledge_sources_list if s.get("type") == "ai_knowledge"]
            if ai_knowledge_sources:
                # Use the highest priority AI knowledge source from config
                ai_source = sorted(ai_knowledge_sources, key=lambda x: x.get("priority", 0), reverse=True)[0]
                ai_source_info = {
                    "source": ai_source.get("name"),
                    "type": ai_source.get("type"),
                    "description": ai_source.get("description")
                }
                if not any(ks["source"] == ai_source_info["source"] for ks in knowledge_sources_used):
                    knowledge_sources_used.append(ai_source_info)
            else:
                # Fallback if not in config
                knowledge_sources_used.append({
                    "source": "AI Best Practices",
                    "type": "ai_knowledge",
                    "description": "General AI coding best practices and patterns"
                })

            user_prompt = f"""Analyze and enhance the following developer prompt. The prompt may be incomplete or lack context.

Original Prompt:
{original_prompt}
{code_context}
{enhancement_instructions}

Please enhance this prompt by:
1. Adding missing technical context
2. Including best practices and coding standards
3. Adding specific requirements that are missing
4. Suggesting edge cases to consider
5. Adding error handling requirements
6. Including performance considerations
7. Adding security considerations
8. Making the prompt clearer and more specific

Format your response as JSON:
{{
    "original_prompt": "{original_prompt}",
    "enhanced_prompt": "enhanced version of the prompt with all improvements",
    "improvements": [
        {{
            "type": "context|requirements|best_practices|edge_cases|error_handling|performance|security",
            "description": "what was added or improved",
            "reason": "why this improvement is important"
        }}
    ],
    "missing_context": ["list of missing context that was added"],
    "suggested_requirements": ["list of suggested requirements"],
    "agent_configuration": {{
        "recommended_temperature": 0.2,
        "recommended_max_tokens": 2000,
        "reasoning": "why these settings are recommended"
    }},
    "confidence_score": 0.95,
    "estimated_quality_improvement": "+35%"
}}"""

            response = self.generate_with_groq(user_prompt, temperature=0.2)

            # Parse response using robust JSON extractor
            from ..utils.json_extractor import extract_json_from_text
            
            extracted = extract_json_from_text(response, fallback_to_text=False)
            
            if isinstance(extracted, dict):
                enhanced_data = extracted
            else:
                # Fallback: create basic structure
                enhanced_data = {
                    "original_prompt": original_prompt,
                    "enhanced_prompt": original_prompt,  # Fallback to original
                    "improvements": [],
                    "missing_context": [],
                    "suggested_requirements": [],
                    "agent_configuration": {
                        "recommended_temperature": 0.2,
                        "recommended_max_tokens": 2000,
                        "reasoning": "Default settings for code generation"
                    },
                    "confidence_score": 0.5,
                    "estimated_quality_improvement": "+0%"
                }
            
            # Add knowledge sources to enhanced data
            enhanced_data["knowledge_sources_used"] = knowledge_sources_used

            # Create suggestion
            suggestion = self.create_suggestion(
                project_id=project_id,
                content=json.dumps(enhanced_data, indent=2)
            )

            self.log_agent_run(
                project_id=project_id,
                status="success",
                result_summary="Enhanced developer prompt"
            )

            return {
                "status": "success",
                "suggestion_id": suggestion.id,
                "enhanced": enhanced_data,
                "message": "Prompt enhanced successfully"
            }

        except Exception as e:
            self.log_agent_run(
                project_id=project_id,
                status="error",
                error_message=str(e)
            )
            return {"status": "error", "error": str(e)}
