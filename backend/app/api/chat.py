"""Chat API routes for global chat interface."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.groq_service import GroqService

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    agent_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    content: str
    agent: Optional[str] = None


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Process a chat message and return AI response.
    
    Args:
        request: Chat request with message and optional agent_id
        
    Returns:
        Chat response with content and agent name
    """
    try:
        groq_service = GroqService()
        
        # Build system prompt based on context
        system_prompt = """You are a helpful AI assistant for Axis Bank's development team.
You have access to:
- Centralized code repository across all microservices
- Jira MCP for project management and tickets
- Multiple AI agents for code generation, security, integration, and more

Provide helpful, accurate, and concise responses. When asked about:
- Code/codebase: Reference specific services and patterns
- Jira tickets: Provide ticket details and status
- Code generation: Offer templates and examples
- Security: Provide security best practices
- Architecture: Explain system design and patterns

Keep responses professional and technical, suitable for enterprise software development."""
        
        # Enhance user prompt with context about selected agent
        user_prompt = request.message
        
        if request.agent_id:
            agent_context = {
                'code-generation': 'Code Generation Agent - specializes in generating microservice boilerplate and business logic',
                'security-guardian': 'Security Guardian Agent - focuses on security compliance, OWASP standards, and vulnerability scanning',
                'integration': 'Integration Agent - handles API contracts, SDKs, and frontend integration code',
                'knowledge': 'Knowledge Agent - provides institutional memory, indexes microservices and patterns',
                'code-template': 'Code Template Agent - offers production-ready service templates and code patterns',
                'prompt-amplifier': 'Prompt Amplifier Agent - enhances developer prompts with best practices',
                'test-data-ui': 'Test Data UI Agent - generates UIs for test data creation',
                'test-case-generator': 'Test Case Generator Agent - creates comprehensive test cases',
                'load-testing': 'Load Testing Agent - handles performance validation and load scenarios',
                'devops': 'DevOps Agent - manages CI/CD pipelines and automated operations',
                'documentation': 'Documentation Agent - generates comprehensive documentation'
            }
            
            agent_info = agent_context.get(request.agent_id, '')
            if agent_info:
                user_prompt = f"Using {agent_info}:\n\n{user_prompt}"
        
        # Generate AI response
        response_text = groq_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,  # Slightly higher for more natural conversation
            max_tokens=1000
        )
        
        # Determine agent name for response
        agent_name = None
        if request.agent_id:
            agent_names = {
                'code-generation': 'Code Generation Agent',
                'security-guardian': 'Security Guardian Agent',
                'integration': 'Integration Agent',
                'knowledge': 'Knowledge Agent',
                'code-template': 'Code Template Agent',
                'prompt-amplifier': 'Prompt Amplifier Agent',
                'test-data-ui': 'Test Data UI Agent',
                'test-case-generator': 'Test Case Generator Agent',
                'load-testing': 'Load Testing Agent',
                'devops': 'DevOps Agent',
                'documentation': 'Documentation Agent'
            }
            agent_name = agent_names.get(request.agent_id)
        
        return ChatResponse(
            content=response_text,
            agent=agent_name
        )
        
    except ValueError as e:
        # Handle missing API key gracefully
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Please set GROQ_API_KEY environment variable."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )
