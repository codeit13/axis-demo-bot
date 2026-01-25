"""Agent API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from ..database import get_db
from ..tables import AgentType
# New agents
from ..agents.business_logic_agent import BusinessLogicAgent
from ..agents.product_requirements_agent import ProductRequirementsAgent
from ..agents.api_contract_agent import APIContractAgent
from ..agents.technical_architecture_agent import TechnicalArchitectureAgent
from ..agents.quality_test_agent import QualityTestAgent
from ..agents.change_impact_agent import ChangeImpactAgent
from ..agents.release_readiness_agent import ReleaseReadinessAgent
# Demo/UI agents
from ..agents.integration_agent import IntegrationAgent
from ..agents.code_template_agent import CodeTemplateAgent
from ..agents.prompt_amplifier_agent import PromptAmplifierAgent
# Legacy agents (for backward compatibility)
from ..agents.unit_test_agent import UnitTestAgent
from ..agents.api_spec_agent import APISpecAgent
from ..agents.bug_scanner_agent import BugScannerAgent
from ..agents.code_review_agent import CodeReviewAgent
from ..agents.documentation_agent import DocumentationAgent

router = APIRouter(prefix="/api/agents", tags=["agents"])


class AnalyzeRequest(BaseModel):
    project_id: int
    code_file_id: Optional[int] = None
    issue_id: Optional[int] = None
    rule_ids: Optional[List[str]] = None
    business_logic_text: Optional[str] = None
    change_type: Optional[str] = None
    release_version: Optional[str] = None
    # Integration Agent params
    service_name: Optional[str] = None
    base_url: Optional[str] = None
    description: Optional[str] = None
    # Code Template Agent params
    template_type: Optional[str] = None
    technologies: Optional[List[str]] = None
    # Prompt Amplifier Agent params
    original_prompt: Optional[str] = None
    context: Optional[str] = None
    agent_config: Optional[Dict[str, Any]] = None
    enhancement_rules: Optional[List[Dict[str, Any]]] = None
    additional_params: Optional[Dict[str, Any]] = {}


def get_agent(agent_type: str, db: Session):
    """Get agent instance by type."""
    try:
        agent_enum = AgentType(agent_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid agent type: {agent_type}")

    agent_map = {
        # New production agents
        AgentType.BUSINESS_LOGIC_POLICY: BusinessLogicAgent,
        AgentType.PRODUCT_REQUIREMENTS: ProductRequirementsAgent,
        AgentType.API_CONTRACT: APIContractAgent,
        AgentType.TECHNICAL_ARCHITECTURE: TechnicalArchitectureAgent,
        AgentType.QUALITY_TEST: QualityTestAgent,
        AgentType.CHANGE_IMPACT: ChangeImpactAgent,
        AgentType.RELEASE_READINESS: ReleaseReadinessAgent,
        # Demo/UI agents
        AgentType.INTEGRATION_AGENT: IntegrationAgent,
        AgentType.CODE_TEMPLATE_AGENT: CodeTemplateAgent,
        AgentType.PROMPT_AMPLIFIER_AGENT: PromptAmplifierAgent,
        # Legacy agents
        AgentType.UNIT_TEST: UnitTestAgent,
        AgentType.API_SPEC: APISpecAgent,
        AgentType.BUG_SCANNER: BugScannerAgent,
        AgentType.CODE_REVIEW: CodeReviewAgent,
        AgentType.DOCUMENTATION: DocumentationAgent,
    }

    agent_class = agent_map.get(agent_enum)
    if not agent_class:
        raise HTTPException(status_code=400, detail=f"Agent type {agent_type} not implemented")

    return agent_class(db)


@router.post("/{agent_type}/analyze")
async def analyze(
    agent_type: str,
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """Run agent analysis."""
    try:
        agent = get_agent(agent_type, db)
        result = agent.analyze(
            project_id=request.project_id,
            code_file_id=request.code_file_id,
            issue_id=request.issue_id,
            rule_ids=request.rule_ids,
            business_logic_text=request.business_logic_text,
            change_type=request.change_type,
            release_version=request.release_version,
            # Integration Agent params
            service_name=request.service_name,
            base_url=request.base_url,
            description=request.description,
            # Code Template Agent params
            template_type=request.template_type,
            technologies=request.technologies,
            # Prompt Amplifier Agent params
            original_prompt=request.original_prompt,
            context=request.context,
            agent_config=request.agent_config,
            enhancement_rules=request.enhancement_rules,
            **request.additional_params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
def get_agent_types():
    """Get list of available agent types."""
    return {
        "agent_types": [
            {
                "value": agent_type.value,
                "name": agent_type.value.replace("_", " ").title()
            }
            for agent_type in AgentType
        ]
    }
