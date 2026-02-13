"""Chat API routes for global chat interface."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
from ..services.groq_service import GroqService
from ..utils.json_extractor import extract_json_from_text

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    agent_id: Optional[str] = None


class MockEndpointItem(BaseModel):
    """Single endpoint in mock payload."""
    method: str
    path: str
    description: str


class MockPayloadModel(BaseModel):
    """Structured mock API payload for Service Virtualization."""
    serviceName: str
    serverUrl: str
    endpoints: List[MockEndpointItem]


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    content: str
    agent: Optional[str] = None
    mock_payload: Optional[Any] = None  # MockPayloadModel when agent is service-virtualization


def _normalize_mock_payload(raw: dict) -> Optional[dict]:
    """Validate and normalize AI-generated mock payload to our schema."""
    if not raw or not isinstance(raw, dict):
        return None
    service_name = raw.get("serviceName") or raw.get("service_name") or "Mock API"
    server_url = raw.get("serverUrl") or raw.get("server_url") or "https://mock.axisbank.com/api/v1"
    endpoints_raw = raw.get("endpoints") or []
    if not isinstance(endpoints_raw, list):
        return None
    endpoints = []
    for ep in endpoints_raw[:20]:  # cap at 20
        if not isinstance(ep, dict):
            continue
        method = (ep.get("method") or "GET").upper()
        if method not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            method = "GET"
        path = ep.get("path") or ep.get("route") or "/data"
        if not str(path).startswith("/"):
            path = "/" + str(path)
        desc = ep.get("description") or ep.get("summary") or f"{method} {path}"
        endpoints.append({"method": method, "path": path, "description": str(desc)})
    if not endpoints:
        endpoints = [{"method": "GET", "path": "/data", "description": "Default mock endpoint"}]
    return {
        "serviceName": str(service_name),
        "serverUrl": str(server_url).rstrip("/"),
        "endpoints": endpoints,
    }


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

        # Service Virtualization: structured mock API payload from AI
        if request.agent_id == "service-virtualization":
            sv_system = """You are a Service Virtualization assistant. Given the user's request, output a mock API design as a single JSON object only (no markdown, no code fences). Use exactly this structure:
{
  "serviceName": "short name for the mock service",
  "serverUrl": "https://mock.axisbank.com/api/v1",
  "endpoints": [
    { "method": "GET", "path": "/resource", "description": "brief description" }
  ]
}
Rules: The base domain for serverUrl MUST be mock.axisbank.com (e.g. https://mock.axisbank.com/api/v1 or https://mock.axisbank.com/v1/...). serviceName and serverUrl are strings; endpoints is an array of objects with method (GET/POST/PUT/PATCH/DELETE), path (must start with /), and description. Infer resources from the user message (e.g. users, payments, orders). Return only the JSON object."""
            sv_prompt = request.message.strip() or "Create a mock API with a few sample endpoints."
            sv_response = groq_service.generate(
                system_prompt=sv_system,
                user_prompt=sv_prompt,
                temperature=0.3,
                max_tokens=800,
            )
            raw = extract_json_from_text(sv_response, fallback_to_text=False)
            mock_payload = _normalize_mock_payload(raw) if isinstance(raw, dict) else None
            if not mock_payload:
                mock_payload = _normalize_mock_payload({
                    "serviceName": "Mock API",
                    "serverUrl": "https://mock.axisbank.com/api/v1",
                    "endpoints": [{"method": "GET", "path": "/data", "description": "Default endpoint"}],
                })
            return ChatResponse(
                content=f"Mock API {mock_payload['serviceName']} is ready. Use the endpoints below.",
                agent="Service Virtualization Agent",
                mock_payload=mock_payload,
            )
        
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
                'documentation': 'Documentation Agent',
                'service-virtualization': 'Service Virtualization Agent',
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
