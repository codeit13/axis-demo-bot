"""Agent orchestration service for managing agent execution flow."""
from typing import List, Dict, Any
from ..tables import AgentType, ChangeType, ChangeImpact


class OrchestrationService:
    """Service for orchestrating agent execution based on changes."""

    # Define agent dependencies
    AGENT_DEPENDENCIES = {
        AgentType.BUSINESS_LOGIC_POLICY: [],  # No dependencies
        AgentType.PRODUCT_REQUIREMENTS: [AgentType.BUSINESS_LOGIC_POLICY],
        AgentType.API_CONTRACT: [AgentType.BUSINESS_LOGIC_POLICY, AgentType.PRODUCT_REQUIREMENTS],
        AgentType.TECHNICAL_ARCHITECTURE: [AgentType.BUSINESS_LOGIC_POLICY, AgentType.PRODUCT_REQUIREMENTS],
        AgentType.QUALITY_TEST: [
            AgentType.BUSINESS_LOGIC_POLICY,
            AgentType.API_CONTRACT,
            AgentType.TECHNICAL_ARCHITECTURE
        ],
        AgentType.CHANGE_IMPACT: [],  # Can run independently
        AgentType.RELEASE_READINESS: [
            AgentType.QUALITY_TEST,
            AgentType.API_CONTRACT
        ]
    }

    # Define which agents are triggered by which change types
    CHANGE_TRIGGERS = {
        ChangeType.BUSINESS_RULE_UPDATE: [
            AgentType.PRODUCT_REQUIREMENTS,
            AgentType.API_CONTRACT,
            AgentType.TECHNICAL_ARCHITECTURE,
            AgentType.QUALITY_TEST,
            AgentType.RELEASE_READINESS
        ],
        ChangeType.API_CONTRACT_CHANGE: [
            AgentType.QUALITY_TEST,
            AgentType.RELEASE_READINESS
        ],
        ChangeType.CODE_CHANGE: [
            AgentType.CHANGE_IMPACT,
            AgentType.QUALITY_TEST
        ],
        ChangeType.ARCHITECTURE_CHANGE: [
            AgentType.QUALITY_TEST,
            AgentType.RELEASE_READINESS
        ]
    }

    @staticmethod
    def get_execution_order(agent_types: List[AgentType]) -> List[AgentType]:
        """
        Get the correct execution order for agents based on dependencies.

        Args:
            agent_types: List of agent types to execute

        Returns:
            Ordered list of agent types
        """
        ordered = []
        remaining = set(agent_types)
        visited = set()

        def visit(agent_type: AgentType):
            if agent_type in visited:
                return
            visited.add(agent_type)

            # Visit dependencies first
            deps = OrchestrationService.AGENT_DEPENDENCIES.get(agent_type, [])
            for dep in deps:
                if dep in remaining:
                    visit(dep)

            if agent_type in remaining:
                ordered.append(agent_type)
                remaining.remove(agent_type)

        # Visit all agents
        for agent_type in list(remaining):
            visit(agent_type)

        return ordered

    @staticmethod
    def get_affected_agents(change_type: ChangeType) -> List[AgentType]:
        """
        Get agents that should be triggered by a change type.

        Args:
            change_type: Type of change

        Returns:
            List of agent types to trigger
        """
        return OrchestrationService.CHANGE_TRIGGERS.get(change_type, [])

    @staticmethod
    def analyze_change_impact(
        change_type: ChangeType,
        affected_rule_ids: List[str],
        affected_agents: List[AgentType]
    ) -> Dict[str, Any]:
        """
        Analyze the impact of a change.

        Args:
            change_type: Type of change
            affected_rule_ids: List of affected Rule IDs
            affected_agents: List of affected agent types

        Returns:
            Impact analysis result
        """
        # Determine risk level
        risk_level = "low"
        if change_type == ChangeType.BUSINESS_RULE_UPDATE:
            risk_level = "high" if len(affected_rule_ids) > 3 else "medium"
        elif change_type == ChangeType.API_CONTRACT_CHANGE:
            risk_level = "high"

        # Get required re-runs
        required_reruns = OrchestrationService.get_execution_order(affected_agents)

        return {
            "change_type": change_type.value,
            "affected_rule_ids": affected_rule_ids,
            "affected_agents": [a.value for a in affected_agents],
            "required_reruns": [a.value for a in required_reruns],
            "risk_level": risk_level,
            "estimated_impact": len(required_reruns)
        }
