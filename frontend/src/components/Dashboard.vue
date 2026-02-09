<template>
  <div class="dashboard-container">
    <div class="content-header">
      <h1 class="page-title">Agents</h1>
      <p class="page-subtitle">Agent Hub</p>
      <p class="page-description">Manage your AI workforce and their permissions.</p>
    </div>

    <!-- Agent Cards Grid -->
    <div class="agents-grid">
      <Card v-for="agent in sortedAgents" :key="agent.id" class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div :class="['agent-icon', agent.iconColor]">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="agent.iconSvg"></svg>
            </div>
            <div class="header-right">
              <div class="agent-stats">
                <div class="stat-item stat-hoverable">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="stat-icon">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
                  <span class="stat-value">{{ getAgentStats(agent.id).users }}</span>
                  <div class="stat-tooltip">
                    <div class="tooltip-content">
                      <div class="tooltip-title">Usage Analytics</div>
                      <div class="tooltip-row">
                        <span class="tooltip-label">Users:</span>
                        <span class="tooltip-number">{{ getAgentStats(agent.id).users }}</span>
            </div>
                      <div class="tooltip-row">
                        <span class="tooltip-label">Total Runs:</span>
                        <span class="tooltip-number">{{ getAgentStats(agent.id).runs || 0 }}</span>
          </div>
                      <div class="tooltip-row">
                        <span class="tooltip-label">Success Rate:</span>
                        <span class="tooltip-number">{{ getAgentStats(agent.id).successRate || 0 }}%</span>
            </div>
          </div>
            </div>
          </div>
                <div class="stat-item stat-hoverable">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="stat-icon">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
                  <span class="stat-value">{{ getAgentStats(agent.id).team }}</span>
                  <div class="stat-tooltip">
                    <div class="tooltip-content">
                      <div class="tooltip-title">Team Information</div>
                      <div class="tooltip-row">
                        <span class="tooltip-label">Team:</span>
                        <span class="tooltip-text">{{ getAgentStats(agent.id).team }}</span>
                      </div>
                      <div class="tooltip-members" v-if="getAgentStats(agent.id).teamMembers && getAgentStats(agent.id).teamMembers.length > 0">
                        <div class="tooltip-label">Members:</div>
                        <div class="tooltip-member-list">
                          <div class="tooltip-member-item" v-for="(member, index) in getAgentStats(agent.id).teamMembers" :key="index">
                            <div class="member-avatar" :style="{ backgroundColor: getMemberColor(member) }">
                              {{ getMemberInitials(member) }}
                            </div>
                            <span class="member-name">{{ member }}</span>
                          </div>
                        </div>
                      </div>
                      <div class="tooltip-desc">Responsible for development & maintenance</div>
                    </div>
            </div>
          </div>
            </div>
            <div class="header-badges">
              <div v-if="agent.actionType === 'openDialog'" class="trending-badge" title="Interactive UI Available">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                  <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                <span>Trending</span>
              </div>
              <Badge variant="default" class="status-badge">ACTIVE</Badge>
            </div>
          </div>
            </div>
          <CardTitle>{{ agent.name }}</CardTitle>
          <p class="agent-subtitle">{{ agent.subtitle }}</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li v-for="(feature, index) in agent.features" :key="index">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>{{ feature }}</span>
            </li>
          </ul>
          <Button variant="default" class="demo-button purple" @click="handleAgentClick(agent)">
            View Demo →
          </Button>
        </CardContent>
      </Card>

      <!-- Deploy New Agent -->
      <Card class="agent-card deploy-card" @click="handleDeployNewAgent">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon purple">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <circle cx="9" cy="9" r="2"></circle>
                <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
              </svg>
            </div>
          </div>
          <CardTitle>Deploy New Agent</CardTitle>
          <p class="agent-subtitle">From Model Registry</p>
        </CardHeader>
        <CardContent>
          <div class="deploy-content">
            <p class="deploy-description">Click to deploy a new agent from the model registry</p>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Global Guardrails Section -->
    <div class="guardrails-section">
      <h2 class="guardrails-title">Global Guardrails</h2>
      <div class="guardrails-list">
        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">Require Human Approval for Production Deploys</h3>
              <p class="guardrail-description">Agents can prepare deployments but cannot execute them without sign-off.</p>
            </div>
            <button 
              class="toggle-switch" 
              :class="{ active: guardrails.humanApproval }"
              @click="guardrails.humanApproval = !guardrails.humanApproval"
            >
              <span class="toggle-slider"></span>
            </button>
          </CardContent>
        </Card>

        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">PII Data Redaction</h3>
              <p class="guardrail-description">Ensure all AI models filter out Personally Identifiable Information from logs.</p>
            </div>
            <button 
              class="toggle-switch" 
              :class="{ active: guardrails.piiRedaction }"
              @click="guardrails.piiRedaction = !guardrails.piiRedaction"
            >
              <span class="toggle-slider"></span>
            </button>
          </CardContent>
        </Card>

        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">Limit Code Generation to Approved Libraries</h3>
              <p class="guardrail-description">Restrict CodeGen Bot to use only verified npm/maven packages from Artifactory.</p>
            </div>
            <button 
              class="toggle-switch" 
              :class="{ active: guardrails.limitLibraries }"
              @click="guardrails.limitLibraries = !guardrails.limitLibraries"
            >
              <span class="toggle-slider"></span>
            </button>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Integration Agent Dialog -->
    <IntegrationAgentDialog :is-open="showIntegrationDialog" @update:open="showIntegrationDialog = $event" />
    
    <!-- Code Template Agent Dialog -->
    <CodeTemplateAgentDialog :is-open="showCodeTemplateDialog" @update:open="showCodeTemplateDialog = $event" />
    
    <!-- Prompt Amplifier Agent Dialog -->
    <PromptAmplifierAgentDialog :is-open="showPromptAmplifierDialog" @update:open="showPromptAmplifierDialog = $event" />
  </div>
</template>

<script>
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import IntegrationAgentDialog from './IntegrationAgentDialog.vue'
import CodeTemplateAgentDialog from './CodeTemplateAgentDialog.vue'
import PromptAmplifierAgentDialog from './PromptAmplifierAgentDialog.vue'

export default {
  name: 'Dashboard',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Badge,
    IntegrationAgentDialog,
    CodeTemplateAgentDialog,
    PromptAmplifierAgentDialog
  },
  data() {
    return {
      showIntegrationDialog: false,
      showCodeTemplateDialog: false,
      showPromptAmplifierDialog: false,
      guardrails: {
        humanApproval: true,
        piiRedaction: true,
        limitLibraries: false
      },
      agents: [
        {
          id: 'code-generation',
          name: 'Code Generation Agent',
          subtitle: 'Intelligent Code Creation',
          iconColor: 'blue',
          iconSvg: '<path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5"></path><path d="M2 12l10 5 10-5"></path>',
          features: [
            'Generates microservice boilerplate and business logic',
            'Learns from existing service patterns',
            'Suggests optimal architecture patterns',
            'Auto-generates unit and integration tests'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'security-guardian',
          name: 'Security Guardian Agent',
          subtitle: 'Compliance & Protection',
          iconColor: 'red',
          iconSvg: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>',
          features: [
            'Enforces security guardrails automatically',
            'Scans for vulnerabilities in real-time',
            'Ensures OWASP compliance',
            'Validates data encryption and authentication'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'integration',
          name: 'Integration Agent',
          subtitle: 'Seamless Connectivity',
          iconColor: 'purple',
          iconSvg: '<rect x="2" y="2" width="8" height="8" rx="2"></rect><rect x="14" y="2" width="8" height="8" rx="2"></rect><rect x="2" y="14" width="8" height="8" rx="2"></rect><rect x="14" y="14" width="8" height="8" rx="2"></rect>',
          features: [
            'Auto-generates API contracts and SDKs',
            'Creates frontend integration code',
            'Maintains API versioning',
            'Generates interactive API documentation'
          ],
          actionType: 'openDialog',
          dialogType: 'integration'
        },
        {
          id: 'knowledge',
          name: 'Knowledge Agent',
          subtitle: 'Institutional Memory',
          iconColor: 'green',
          iconSvg: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>',
          features: [
            'Indexes all microservices and patterns',
            'Suggests reusable components',
            'Provides context-aware recommendations',
            'Maintains design pattern library'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'code-template',
          name: 'Code Template Agent',
          subtitle: 'Reusable Code Library',
          iconColor: 'blue',
          iconSvg: '<polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline>',
          features: [
            'Provides production-ready service templates',
            'Maintains standardized code patterns',
            'Includes complete project scaffolding',
            'Follows Axis Bank coding standards'
          ],
          actionType: 'openDialog',
          dialogType: 'code-template'
        },
        {
          id: 'prompt-amplifier',
          name: 'Prompt Amplifier Agent',
          subtitle: 'Developer Enablement',
          iconColor: 'purple',
          iconSvg: '<polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>',
          features: [
            'Enhances prompts from junior developers',
            'Adds missing context and best practices',
            'Suggests clearer technical requirements',
            'Guides developers to write better prompts'
          ],
          actionType: 'openDialog',
          dialogType: 'prompt-amplifier'
        },
        {
          id: 'test-data-ui',
          name: 'Test Data UI Agent',
          subtitle: 'Testing Environment Control',
          iconColor: 'teal',
          iconSvg: '<rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line>',
          features: [
            'Generates intuitive UIs for test data creation',
            'Provides feature flag management interface',
            'Creates mock data generators for scenarios',
            'Enables real-time configuration changes'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'test-case-generator',
          name: 'Test Case Generator Agent',
          subtitle: 'Intelligent Test Coverage',
          iconColor: 'red',
          iconSvg: '<rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line>',
          features: [
            'Analyzes code to suggest comprehensive test cases',
            'Generates edge case and boundary tests',
            'Creates regression test suites automatically',
            'Identifies untested code paths'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'load-testing',
          name: 'Load Testing Agent',
          subtitle: 'Performance Validation',
          iconColor: 'orange',
          iconSvg: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
          features: [
            'Simulates realistic load scenarios',
            'Identifies performance bottlenecks',
            'Generates scalability recommendations',
            'Auto-tunes resource configurations'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'devops',
          name: 'DevOps Agent',
          subtitle: 'Automated Operations',
          iconColor: 'orange',
          iconSvg: '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>',
          features: [
            'CI/CD pipeline configuration',
            'Auto-scaling and monitoring setup',
            'Performance optimization suggestions',
            'Automated rollback on failures'
          ],
          actionType: 'viewDemo'
        },
        {
          id: 'documentation',
          name: 'Documentation Agent',
          subtitle: 'Standardized Knowledge',
          iconColor: 'blue',
          iconSvg: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path><path d="M8 7h8M8 11h8M8 15h4"></path>',
          features: [
            'Auto-generates comprehensive docs',
            'Creates diagrams and flowcharts',
            'Maintains changelog and versioning',
            'Generates onboarding guides'
          ],
          actionType: 'viewDemo'
        }
      ],
      agentStats: {
        'code-generation': { 
          users: 142, 
          team: 'Platform Team',
          teamMembers: ['Rajesh Kumar', 'Priya Sharma', 'Amit Mishra'],
          runs: 1247,
          successRate: 94
        },
        'security-guardian': { 
          users: 89, 
          team: 'Security Team',
          teamMembers: ['Vikram Tiwari', 'Sneha Reddy'],
          runs: 892,
          successRate: 97
        },
        'integration': { 
          users: 312, 
          team: 'Integration Team',
          teamMembers: ['Anjali Patel', 'Rohit Desai', 'Kavita Nair'],
          runs: 3456,
          successRate: 95
        },
        'knowledge': { 
          users: 156, 
          team: 'Architecture Team',
          teamMembers: ['Arjun Singh', 'Meera Verma', 'Suresh Kapoor'],
          runs: 1834,
          successRate: 96
        },
        'code-template': { 
          users: 289, 
          team: 'Platform Team',
          teamMembers: ['Rajesh Kumar', 'Priya Sharma', 'Amit Mishra'],
          runs: 2456,
          successRate: 98
        },
        'prompt-amplifier': { 
          users: 356, 
          team: 'DevOps Team',
          teamMembers: ['Ravi Mehta', 'Deepa Lakshmi', 'Nikhil Pandey'],
          runs: 4421,
          successRate: 94
        },
        'test-data-ui': { 
          users: 98, 
          team: 'QA Team',
          teamMembers: ['Sunita Gupta', 'Manoj Rao'],
          runs: 756,
          successRate: 95
        },
        'test-case-generator': { 
          users: 112, 
          team: 'QA Team',
          teamMembers: ['Sunita Gupta', 'Manoj Rao', 'Pooja Khanna'],
          runs: 1023,
          successRate: 92
        },
        'load-testing': { 
          users: 67, 
          team: 'Performance Team',
          teamMembers: ['Kiran Bansal', 'Aditya Shah'],
          runs: 445,
          successRate: 89
        },
        'devops': { 
          users: 145, 
          team: 'DevOps Team',
          teamMembers: ['Ravi Mehta', 'Deepa Lakshmi', 'Nikhil Pandey'],
          runs: 1234,
          successRate: 96
        },
        'documentation': { 
          users: 91, 
          team: 'Documentation Team',
          teamMembers: ['Shruti Agarwal', 'Varun Thakur'],
          runs: 678,
          successRate: 97
        }
      }
    }
  },
  computed: {
    sortedAgents() {
      // Sort agents by user count (highest first)
      return [...this.agents].sort((a, b) => {
        const aUsers = this.getAgentStats(a.id).users || 0
        const bUsers = this.getAgentStats(b.id).users || 0
        return bUsers - aUsers
      })
    }
  },
  methods: {
    openIntegrationDialog() {
      this.showIntegrationDialog = true
    },
    openCodeTemplateDialog() {
      this.showCodeTemplateDialog = true
    },
    openPromptAmplifierDialog() {
      this.showPromptAmplifierDialog = true
    },
    handleDeployNewAgent() {
      // TODO: Implement deploy new agent functionality
      alert('Deploy New Agent functionality coming soon!')
    },
    viewDemo(agentType) {
      if (agentType === 'integration') {
        this.openIntegrationDialog()
      } else if (agentType === 'template' || agentType === 'code-template') {
        this.openCodeTemplateDialog()
      } else if (agentType === 'prompt' || agentType === 'prompt-amplifier') {
        this.openPromptAmplifierDialog()
      } else {
        // For other agents, show a placeholder message
        // In the future, these can have their own dialog components
        alert(`${this.getAgentDisplayName(agentType)} demo coming soon!`)
      }
    },
    getAgentDisplayName(agentType) {
      const names = {
        'code-generation': 'Code Generation Agent',
        'security-guardian': 'Security Guardian Agent',
        'knowledge': 'Knowledge Agent',
        'test-data-ui': 'Test Data UI Agent',
        'test-case-generator': 'Test Case Generator Agent',
        'load-testing': 'Load Testing Agent',
        'devops': 'DevOps Agent',
        'documentation': 'Documentation Agent'
      }
      return names[agentType] || agentType
    },
    getAgentStats(agentType) {
      return this.agentStats[agentType] || { users: 0, team: 'N/A', teamMembers: [], runs: 0, successRate: 0 }
    },
    getMemberInitials(name) {
      if (!name) return '?'
      const parts = name.split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    },
    getMemberColor(name) {
      // Generate a consistent color based on the name
      const colors = [
        '#97144D', '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
        '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16', '#f97316'
      ]
      let hash = 0
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
      }
      return colors[Math.abs(hash) % colors.length]
    },
    handleAgentClick(agent) {
      if (agent.actionType === 'openDialog') {
        if (agent.dialogType === 'integration') {
          this.openIntegrationDialog()
        } else if (agent.dialogType === 'code-template') {
          this.openCodeTemplateDialog()
        } else if (agent.dialogType === 'prompt-amplifier') {
          this.openPromptAmplifierDialog()
        }
      } else {
        this.viewDemo(agent.id)
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100%;
}

.content-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.page-description {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Agents Grid */
.agents-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .agents-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .agents-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 640px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .content-header {
    margin-bottom: 1.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
}

.agent-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  transition: box-shadow 0.2s;
}

.agent-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.agent-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.agent-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.agent-icon.blue {
  background-color: #dbeafe;
  color: #3b82f6;
}

.agent-icon.red {
  background-color: #fee2e2;
  color: #ef4444;
}

.agent-icon.purple {
  background-color: #f3e8ff;
  color: #97144D;
}

.agent-icon.green {
  background-color: #d1fae5;
  color: #10b981;
}

.agent-icon.teal {
  background-color: #ccfbf1;
  color: #14b8a6;
}

.agent-icon.orange {
  background-color: #fed7aa;
  color: #f97316;
}

.header-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-badge {
  background-color: #10b981;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.trending-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
  animation: pulse-glow 2s ease-in-out infinite;
}

.trending-badge svg {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
  }
  50% {
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
  }
}

.coming-soon-badge {
  background-color: #9ca3af;
  color: white;
}

.agent-card.coming-soon {
  opacity: 0.7;
  position: relative;
}

.agent-card.coming-soon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  pointer-events: none;
  border-radius: 8px;
}

.agent-card.coming-soon .agent-icon {
  opacity: 0.6;
}

.agent-card.coming-soon .agent-subtitle {
  color: #9ca3af;
}

.agent-card.coming-soon .features-list {
  opacity: 0.8;
}

.agent-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #374151;
}

.check-icon {
  color: #10b981;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

/* Agent Stats */
.agent-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  position: relative;
  z-index: 1;
}

.stat-item:hover {
  z-index: 10001;
}

.stat-hoverable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-hoverable:hover {
  transform: translateY(-1px);
}

.stat-hoverable:hover .stat-icon {
  color: #97144D;
}

.stat-hoverable:hover .stat-value {
  color: #97144D;
}

.stat-icon {
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.stat-value {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  white-space: nowrap;
  transition: color 0.2s ease;
}

/* Stat Tooltip */
.stat-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(-8px);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
  z-index: 10000;
  margin-bottom: 8px;
}

.stat-hoverable:hover .stat-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
  pointer-events: auto;
}

.tooltip-content {
  background: #1f2937;
  color: white;
  padding: 0.625rem 0.875rem;
  border-radius: 8px;
  font-size: 0.75rem;
  min-width: 160px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  position: relative;
  white-space: nowrap;
}

.tooltip-content::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: #1f2937;
}

.tooltip-title {
  font-size: 0.625rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  font-weight: 600;
  white-space: nowrap;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.375rem;
  gap: 0.5rem;
}

.tooltip-row:last-child {
  margin-bottom: 0;
}

.tooltip-label {
  font-size: 0.75rem;
  color: #d1d5db;
  white-space: nowrap;
}

.tooltip-number {
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
  white-space: nowrap;
}

.tooltip-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

.tooltip-value {
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.125rem;
}

.tooltip-desc {
  font-size: 0.625rem;
  color: #d1d5db;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  white-space: nowrap;
}

.tooltip-members {
  margin-top: 0.5rem;
}

.tooltip-member-list {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-top: 0.375rem;
}

.tooltip-member-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.member-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.member-name {
  font-size: 0.75rem;
  color: white;
  white-space: nowrap;
}

.demo-button {
  margin-top: 1rem;
  width: 100%;
}

.demo-button.purple {
  background-color: #97144D;
  color: white;
}

.demo-button.purple:hover {
  background-color: #7a0f3d;
}

.demo-button.blue {
  background-color: #3b82f6;
  color: white;
}

.demo-button.blue:hover {
  background-color: #2563eb;
}

/* Deploy New Agent Card */
.deploy-card {
  border: 2px dashed #d1d5db;
  cursor: pointer;
  transition: all 0.2s;
}

.deploy-card:hover {
  border-color: #97144D;
  background-color: #fef7ff;
}

.deploy-content {
  text-align: center;
  padding: 1rem 0;
}

.deploy-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

/* Global Guardrails Section */
.guardrails-section {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e5e5;
}

.guardrails-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.guardrails-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.guardrail-card {
  background: white;
  border: 1px solid #e5e5e5;
}

.guardrail-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  gap: 2rem;
}

.guardrail-info {
  flex: 1;
}

.guardrail-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.guardrail-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  width: 52px;
  height: 28px;
  background-color: #d1d5db;
  border-radius: 14px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  flex-shrink: 0;
}

.toggle-switch.active {
  background-color: #10b981;
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 24px;
  height: 24px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch.active .toggle-slider {
  transform: translateX(24px);
}

.toggle-switch:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(151, 20, 77, 0.1);
}

@media (max-width: 768px) {
  .guardrail-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .toggle-switch {
    align-self: flex-end;
  }
}
</style>
