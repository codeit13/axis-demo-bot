<template>
  <div class="dashboard-wrapper">
    <Tabs v-model="activeTab" class="tabs-root">
      <div class="tabs-bar">
        <TabsList class="top-tabs-list">
          <TabsTrigger value="hub" class="top-tab-trigger">
            Agent Hub
          </TabsTrigger>
          <TabsTrigger value="chat" class="top-tab-trigger">
            Chat Mode
          </TabsTrigger>
        </TabsList>
      </div>

      <TabsContent value="chat" class="tab-content-chat">
        <Chat />
      </TabsContent>

      <TabsContent value="hub" class="tab-content-hub">
        <div class="dashboard-container">
      <div class="content-header">
        <h1 class="page-title">Agents</h1>
        <p class="page-subtitle">Agent Hub</p>
        <p class="page-description">Manage your AI workforce and their permissions.</p>
      </div>

      <!-- Agent Accordions Grid -->
    <div class="agents-grid">
      <div v-for="agent in sortedAgents" :key="agent.id" class="agent-accordion-card">
        <Accordion type="single" collapsible>
          <AccordionItem :value="agent.id" class="agent-accordion-item">
            <AccordionTrigger class="agent-accordion-trigger">
              <div class="accordion-trigger-content">
                <div class="accordion-left">
                  <div :class="['agent-icon', agent.iconColor]">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      v-html="agent.iconSvg"></svg>
                  </div>
                  <span class="accordion-agent-name">{{ agent.name }}</span>
                </div>
                <div class="accordion-right">
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
            </AccordionTrigger>
            <AccordionContent>
              <div class="accordion-body">
                <p class="accordion-agent-subtitle">{{ agent.subtitle }}</p>
                <ul class="features-list">
                  <li v-for="(feature, index) in agent.features" :key="index">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      class="check-icon">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span>{{ feature }}</span>
                  </li>
                </ul>
                <Button variant="default" class="demo-button purple" @click="handleAgentClick(agent)">
                  View Demo →
                </Button>
                <div class="accordion-analytics">
                  <div class="analytics-row">
                    <div
                      class="stat-item stat-hoverable"
                      @mouseenter="showStatTooltip($event, 'usage', agent.id)"
                      @mouseleave="hideStatTooltip"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                        class="stat-icon">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                      <span class="stat-label">Users</span>
                      <span class="stat-value">{{ getAgentStats(agent.id).users }}</span>
                    </div>
                    
                    <div
                      class="stat-item stat-hoverable"
                      @mouseenter="showStatTooltip($event, 'team', agent.id)"
                      @mouseleave="hideStatTooltip"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                        class="stat-icon">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                      </svg>
                      <span class="stat-label">Team</span>
                      <span class="stat-value">{{ getAgentStats(agent.id).team }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>

      <!-- Deploy New Agent -->
      <div class="agent-accordion-card deploy-card" @click="handleDeployNewAgent">
        <div class="deploy-card-inner">
          <div class="agent-icon purple">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </div>
          <div class="deploy-text">
            <span class="deploy-title">Deploy New Agent</span>
            <span class="deploy-subtitle">From Model Registry</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Global Guardrails Section -->
    <div class="guardrails-section">
      <h2 class="guardrails-title">Global Guardrails</h2>
      <div class="guardrails-list">
        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">Require Human Approval for Production Deploys</h3>
              <p class="guardrail-description">Agents can prepare deployments but cannot execute them without sign-off.
              </p>
            </div>
            <button class="toggle-switch" :class="{ active: guardrails.humanApproval }"
              @click="guardrails.humanApproval = !guardrails.humanApproval">
              <span class="toggle-slider"></span>
            </button>
          </CardContent>
        </Card>

        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">PII Data Redaction</h3>
              <p class="guardrail-description">Ensure all AI models filter out Personally Identifiable Information from
                logs.</p>
            </div>
            <button class="toggle-switch" :class="{ active: guardrails.piiRedaction }"
              @click="guardrails.piiRedaction = !guardrails.piiRedaction">
              <span class="toggle-slider"></span>
            </button>
          </CardContent>
        </Card>

        <Card class="guardrail-card">
          <CardContent class="guardrail-content">
            <div class="guardrail-info">
              <h3 class="guardrail-name">Limit Code Generation to Approved Libraries</h3>
              <p class="guardrail-description">Restrict CodeGen Bot to use only verified npm/maven packages from
                Artifactory.</p>
            </div>
            <button class="toggle-switch" :class="{ active: guardrails.limitLibraries }"
              @click="guardrails.limitLibraries = !guardrails.limitLibraries">
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
      <PromptAmplifierAgentDialog :is-open="showPromptAmplifierDialog"
        @update:open="showPromptAmplifierDialog = $event" />

      <!-- Service Virtualization Agent Dialog -->
      <ServiceVirtualizationAgentDialog :is-open="showServiceVirtualizationDialog"
        @update:open="showServiceVirtualizationDialog = $event" />

    <!-- Portaled stat tooltips (never clipped by overflow) -->
    <Teleport to="body">
      <Transition name="tooltip-fade">
        <div
          v-if="statTooltip.show && statTooltip.agentId"
          class="stat-tooltip-portal"
          :style="{
            left: statTooltip.x + 'px',
            top: statTooltip.y + 'px'
          }"
          @mouseenter="clearStatTooltipHide"
          @mouseleave="hideStatTooltip(true)"
        >
          <div class="tooltip-content" v-if="statTooltip.type === 'usage'">
            <div class="tooltip-title">Usage Analytics</div>
            <div class="tooltip-row">
              <span class="tooltip-label">Users:</span>
              <span class="tooltip-number">{{ getAgentStats(statTooltip.agentId).users }}</span>
            </div>
            <div class="tooltip-row">
              <span class="tooltip-label">Total Runs:</span>
              <span class="tooltip-number">{{ getAgentStats(statTooltip.agentId).runs || 0 }}</span>
            </div>
            <div class="tooltip-row">
              <span class="tooltip-label">Success Rate:</span>
              <span class="tooltip-number">{{ getAgentStats(statTooltip.agentId).successRate || 0 }}%</span>
            </div>
          </div>
          <div class="tooltip-content" v-else-if="statTooltip.type === 'team'">
            <div class="tooltip-title">Team Information</div>
            <div class="tooltip-row">
              <span class="tooltip-label">Team:</span>
              <span class="tooltip-text">{{ getAgentStats(statTooltip.agentId).team }}</span>
            </div>
            <div class="tooltip-members"
              v-if="getAgentStats(statTooltip.agentId).teamMembers && getAgentStats(statTooltip.agentId).teamMembers.length > 0">
              <div class="tooltip-label">Members:</div>
              <div class="tooltip-member-list">
                <div class="tooltip-member-item"
                  v-for="(member, index) in getAgentStats(statTooltip.agentId).teamMembers" :key="index">
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
      </Transition>
    </Teleport>
        </div>
      </TabsContent>
    </Tabs>
  </div>
</template>

<script>
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from './ui/accordion'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Card, CardContent } from './ui/card'
import IntegrationAgentDialog from './IntegrationAgentDialog.vue'
import CodeTemplateAgentDialog from './CodeTemplateAgentDialog.vue'
import PromptAmplifierAgentDialog from './PromptAmplifierAgentDialog.vue'
import ServiceVirtualizationAgentDialog from './ServiceVirtualizationAgentDialog.vue'
import Chat from './Chat.vue'

export default {
  name: 'Dashboard',
  components: {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
    Button,
    Badge,
    Card,
    CardContent,
    IntegrationAgentDialog,
    CodeTemplateAgentDialog,
    PromptAmplifierAgentDialog,
    ServiceVirtualizationAgentDialog,
    Chat
  },
  data() {
    return {
      activeTab: 'hub',
      showIntegrationDialog: false,
      showCodeTemplateDialog: false,
      showPromptAmplifierDialog: false,
      showServiceVirtualizationDialog: false,
      statTooltip: { show: false, type: 'usage', agentId: null, x: 0, y: 0 },
      statTooltipHideTimeout: null,
      guardrails: {
        humanApproval: true,
        piiRedaction: true,
        limitLibraries: false
      },
      agents: [
        {
          id: 'service-virtualization',
          name: 'Service Virtualization Agent',
          subtitle: 'Instant Mock APIs',
          iconColor: 'teal',
          iconSvg: '<circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>',
          features: [
            'Creates mock APIs instantly for any service',
            'Generates realistic response data with AI',
            'Simulates latency, errors, and edge cases',
            'Exports to Postman & OpenAPI formats'
          ],
          actionType: 'openDialog',
          dialogType: 'service-virtualization'
        },
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
        'service-virtualization': {
          users: 423,
          team: 'Platform Team',
          teamMembers: ['Rajesh Kumar', 'Priya Sharma', 'Vikram Tiwari', 'Sneha Reddy'],
          runs: 5890,
          successRate: 99
        },
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
    openServiceVirtualizationDialog() {
      this.showServiceVirtualizationDialog = true
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
      } else if (agentType === 'service-virtualization') {
        this.openServiceVirtualizationDialog()
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
    showStatTooltip(event, type, agentId) {
      if (this.statTooltipHideTimeout) {
        clearTimeout(this.statTooltipHideTimeout)
        this.statTooltipHideTimeout = null
      }
      const el = event && event.currentTarget
      if (el) {
        const rect = el.getBoundingClientRect()
        this.statTooltip = {
          show: true,
          type,
          agentId,
          x: rect.left + rect.width / 2,
          y: rect.top
        }
      } else if (agentId && this.statTooltip.show) {
        this.statTooltip = { ...this.statTooltip, agentId, type }
      }
    },
    hideStatTooltip(immediate = false) {
      if (this.statTooltipHideTimeout) {
        clearTimeout(this.statTooltipHideTimeout)
        this.statTooltipHideTimeout = null
      }
      if (immediate) {
        this.statTooltip = { show: false, type: 'usage', agentId: null, x: 0, y: 0 }
      } else {
        this.statTooltipHideTimeout = setTimeout(() => {
          this.statTooltip = { show: false, type: 'usage', agentId: null, x: 0, y: 0 }
          this.statTooltipHideTimeout = null
        }, 120)
      }
    },
    clearStatTooltipHide() {
      if (this.statTooltipHideTimeout) {
        clearTimeout(this.statTooltipHideTimeout)
        this.statTooltipHideTimeout = null
      }
    },
    handleAgentClick(agent) {
      if (agent.actionType === 'openDialog') {
        if (agent.dialogType === 'integration') {
          this.openIntegrationDialog()
        } else if (agent.dialogType === 'code-template') {
          this.openCodeTemplateDialog()
        } else if (agent.dialogType === 'prompt-amplifier') {
          this.openPromptAmplifierDialog()
        } else if (agent.dialogType === 'service-virtualization') {
          this.openServiceVirtualizationDialog()
        }
      } else {
        this.viewDemo(agent.id)
      }
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 73px);
  background-color: #f5f5f5;
}

.tabs-root {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.tabs-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e5e5;
  flex-shrink: 0;
}

.top-tabs-list {
  display: flex;
  gap: 0.25rem;
  background: #f3f4f6;
  padding: 0.25rem;
  flex-shrink: 0;
  height: auto;
  border-radius: 9999px;
  width: auto;
  justify-content: center;
  border: 1px solid #e5e7eb;
}

.top-tab-trigger {
  padding: 0.625rem 1.75rem;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6b7280;
  background: transparent;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  box-shadow: none;
  letter-spacing: 0.01em;
}

.top-tab-trigger:hover {
  color: #374151;
  background: rgba(0, 0, 0, 0.04);
}

.top-tab-trigger[data-state="active"] {
  color: #97144D;
  background: white;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
}

.tab-content-chat {
  flex: 1;
  min-height: 0;
  margin-top: 0;
}

.tab-content-chat[data-state="active"] {
  display: flex;
  flex-direction: column;
}

.tab-content-chat :deep(.chat-container) {
  flex: 1;
  min-height: 0;
  height: auto;
}

.tab-content-hub {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  margin-top: 0;
}

.dashboard-container {
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 0;
  flex: 1;
  overflow-y: auto;
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
  max-width: 100%;
  overflow: visible;
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

.agent-accordion-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  align-self: start;
  min-width: 0;
  position: relative;
}

.agent-accordion-item {
  border-bottom: none;
}

.agent-accordion-card :deep(button) {
  padding: 1rem 1.5rem;
  background: white;
  transition: background-color 0.15s;
}

.agent-accordion-card :deep(button):hover {
  background: #f9fafb;
}

.agent-accordion-card :deep([data-state=open]) {
  overflow: visible;
}

.agent-accordion-card :deep([data-state=open]) > div {
  overflow: visible;
}

/* Allow the accordion content panel to show tooltips outside (avoid clipping) */
.agent-accordion-card :deep(.overflow-hidden:has(.accordion-body)) {
  overflow: visible;
}

.accordion-trigger-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 0.75rem;
  min-width: 0;
}

.accordion-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1;
}

.accordion-agent-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.accordion-agent-subtitle {
  font-size: 0.8125rem;
  color: #6b7280;
  margin: 0 0 0.75rem 0;
}

.accordion-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.accordion-body {
  padding: 0 1.5rem 0.5rem;
  min-width: 0;
  overflow: visible;
}

.accordion-analytics {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.analytics-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.stat-label {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-right: -0.125rem;
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

  .accordion-trigger-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .accordion-right {
    margin-left: auto;
  }

  .analytics-row {
    gap: 1rem;
  }
}

.agent-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
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

  0%,
  100% {
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
  }

  50% {
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
  }
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

/* Stat Tooltip (portaled to body so never clipped) */
.stat-tooltip-portal {
  position: fixed;
  transform: translate(-50%, -100%) translateY(-8px);
  z-index: 99999;
  pointer-events: auto;
}

.stat-tooltip-portal.tooltip-fade-enter-active,
.stat-tooltip-portal.tooltip-fade-leave-active {
  transition: opacity 0.15s ease;
}
.stat-tooltip-portal.tooltip-fade-enter-from,
.stat-tooltip-portal.tooltip-fade-leave-to {
  opacity: 0;
}

.tooltip-content {
  background: #1f2937;
  color: white;
  padding: 0.625rem 0.875rem;
  border-radius: 8px;
  font-size: 0.75rem;
  min-width: 160px;
  max-width: 260px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  position: relative;
  white-space: normal;
  word-break: break-word;
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
}

.tooltip-number {
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
}

.tooltip-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
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
  min-width: 0;
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

/* Deploy New Agent */
.deploy-card {
  border: 2px dashed #d1d5db;
  cursor: pointer;
  transition: all 0.15s;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
}

.deploy-card:hover {
  border-color: #97144D;
  background-color: #fef7ff;
}

.deploy-card-inner {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.deploy-text {
  display: flex;
  flex-direction: column;
}

.deploy-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #97144D;
}

.deploy-subtitle {
  font-size: 0.8125rem;
  color: #6b7280;
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
