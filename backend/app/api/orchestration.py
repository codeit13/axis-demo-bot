"""Agent Orchestration API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..tables import AgentType, ChangeType
from ..services.orchestration_service import OrchestrationService
from ..agents.business_logic_agent import BusinessLogicAgent
from ..agents.product_requirements_agent import ProductRequirementsAgent
from ..agents.api_contract_agent import APIContractAgent
from ..agents.technical_architecture_agent import TechnicalArchitectureAgent
from ..agents.quality_test_agent import QualityTestAgent
from ..agents.change_impact_agent import ChangeImpactAgent
from ..agents.release_readiness_agent import ReleaseReadinessAgent

router = APIRouter(prefix="/api/orchestration", tags=["orchestration"])


class OrchestrationRequest(BaseModel):
    project_id: int
    agent_types: List[str]  # List of agent types to run
    rule_ids: Optional[List[str]] = None
    code_file_id: Optional[int] = None
    change_type: Optional[str] = None
    release_version: Optional[str] = None


@router.post("/run-sequence")
async def run_agent_sequence(
    request: OrchestrationRequest,
    db: Session = Depends(get_db)
):
    """
    Run agents in the correct execution order based on dependencies.
    
    This endpoint orchestrates agent execution by:
    1. Determining the correct execution order based on dependencies
    2. Running agents sequentially
    3. Passing results from one agent to the next when applicable
    """
    try:
        # Convert agent type strings to enums
        agent_enums = []
        for agent_type_str in request.agent_types:
            try:
                agent_enum = AgentType(agent_type_str)
                agent_enums.append(agent_enum)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid agent type: {agent_type_str}"
                )

        # Get execution order
        execution_order = OrchestrationService.get_execution_order(agent_enums)

        results = []
        last_result = None

        for agent_type in execution_order:
            # Get agent instance
            agent_map = {
                AgentType.BUSINESS_LOGIC_POLICY: BusinessLogicAgent,
                AgentType.PRODUCT_REQUIREMENTS: ProductRequirementsAgent,
                AgentType.API_CONTRACT: APIContractAgent,
                AgentType.TECHNICAL_ARCHITECTURE: TechnicalArchitectureAgent,
                AgentType.QUALITY_TEST: QualityTestAgent,
                AgentType.CHANGE_IMPACT: ChangeImpactAgent,
                AgentType.RELEASE_READINESS: ReleaseReadinessAgent,
            }

            agent_class = agent_map.get(agent_type)
            if not agent_class:
                results.append({
                    "agent_type": agent_type.value,
                    "status": "skipped",
                    "message": "Agent not implemented"
                })
                continue

            agent = agent_class(db)

            # Prepare parameters
            params = {
                "project_id": request.project_id,
                "code_file_id": request.code_file_id,
                "rule_ids": request.rule_ids
            }

            # Add agent-specific parameters
            if agent_type == AgentType.BUSINESS_LOGIC_POLICY:
                # Extract business logic text from previous result if available
                if last_result and "business_logic_text" in last_result:
                    params["business_logic_text"] = last_result["business_logic_text"]
            elif agent_type == AgentType.CHANGE_IMPACT:
                params["change_type"] = request.change_type or ChangeType.BUSINESS_RULE_UPDATE.value
            elif agent_type == AgentType.RELEASE_READINESS:
                params["release_version"] = request.release_version

            # Run agent
            try:
                result = agent.analyze(**params)
                result["agent_type"] = agent_type.value
                results.append(result)
                last_result = result
            except Exception as e:
                results.append({
                    "agent_type": agent_type.value,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "status": "completed",
            "execution_order": [a.value for a in execution_order],
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger-by-change")
async def trigger_agents_by_change(
    project_id: int,
    change_type: str,
    rule_ids: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger agents based on a change type.
    
    This endpoint:
    1. Analyzes the change impact
    2. Determines which agents need to be re-run
    3. Executes them in the correct order
    """
    try:
        # First, run change impact analysis
        change_impact_agent = ChangeImpactAgent(db)
        impact_result = change_impact_agent.analyze(
            project_id=project_id,
            change_type=change_type,
            rule_ids=rule_ids or []
        )

        if impact_result.get("status") != "success":
            return {
                "status": "error",
                "message": "Change impact analysis failed",
                "error": impact_result.get("error")
            }

        # Get required re-runs from impact result
        required_reruns = impact_result.get("required_reruns", [])
        
        if not required_reruns:
            return {
                "status": "completed",
                "message": "No agents need to be re-run",
                "impact_analysis": impact_result
            }

        # Convert to agent enums
        agent_enums = []
        for agent_type_str in required_reruns:
            try:
                agent_enum = AgentType(agent_type_str)
                agent_enums.append(agent_enum)
            except ValueError:
                continue

        # Get execution order
        execution_order = OrchestrationService.get_execution_order(agent_enums)

        # Run agents
        results = []
        for agent_type in execution_order:
            agent_map = {
                AgentType.PRODUCT_REQUIREMENTS: ProductRequirementsAgent,
                AgentType.API_CONTRACT: APIContractAgent,
                AgentType.TECHNICAL_ARCHITECTURE: TechnicalArchitectureAgent,
                AgentType.QUALITY_TEST: QualityTestAgent,
                AgentType.RELEASE_READINESS: ReleaseReadinessAgent,
            }

            agent_class = agent_map.get(agent_type)
            if not agent_class:
                continue

            agent = agent_class(db)
            params = {
                "project_id": project_id,
                "rule_ids": rule_ids
            }

            try:
                result = agent.analyze(**params)
                result["agent_type"] = agent_type.value
                results.append(result)
            except Exception as e:
                results.append({
                    "agent_type": agent_type.value,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "status": "completed",
            "change_impact": impact_result,
            "triggered_agents": [a.value for a in execution_order],
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
