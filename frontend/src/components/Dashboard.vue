<template>
  <div class="dashboard-container">
    <div class="content-header">
      <h1 class="page-title">Agents</h1>
      <p class="page-subtitle">Agent Hub</p>
      <p class="page-description">Manage your AI workforce and their permissions.</p>
    </div>

    <!-- Agent Cards Grid -->
    <div class="agents-grid">
      <!-- Code Generation Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon blue">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Code Generation Agent</CardTitle>
          <p class="agent-subtitle">Intelligent Code Creation</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates microservice boilerplate and business logic</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Learns from existing service patterns</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Suggests optimal architecture patterns</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Auto-generates unit and integration tests</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Security Guardian Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon red">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Security Guardian Agent</CardTitle>
          <p class="agent-subtitle">Compliance & Protection</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Enforces security guardrails automatically</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Scans for vulnerabilities in real-time</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Ensures OWASP compliance</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Validates data encryption and authentication</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Integration Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon purple">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="8" height="8" rx="2"></rect>
                <rect x="14" y="2" width="8" height="8" rx="2"></rect>
                <rect x="2" y="14" width="8" height="8" rx="2"></rect>
                <rect x="14" y="14" width="8" height="8" rx="2"></rect>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Integration Agent</CardTitle>
          <p class="agent-subtitle">Seamless Connectivity</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Auto-generates API contracts and SDKs</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Creates frontend integration code</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Maintains API versioning</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates interactive API documentation</span>
            </li>
          </ul>
          <Button variant="default" class="demo-button purple" @click="openIntegrationDialog">
            View Demo →
          </Button>
        </CardContent>
      </Card>

      <!-- Knowledge Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon green">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Knowledge Agent</CardTitle>
          <p class="agent-subtitle">Institutional Memory</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Indexes all microservices and patterns</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Suggests reusable components</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Provides context-aware recommendations</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Maintains design pattern library</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Code Template Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon blue">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Code Template Agent</CardTitle>
          <p class="agent-subtitle">Reusable Code Library</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Provides production-ready service templates</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Maintains standardized code patterns</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Includes complete project scaffolding</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Follows Axis Bank coding standards</span>
            </li>
          </ul>
          <Button variant="default" class="demo-button blue" @click="openCodeTemplateDialog">
            View Demo →
          </Button>
        </CardContent>
      </Card>

      <!-- Prompt Amplifier Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon purple">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
            </div>
            <Badge variant="default" class="status-badge">ACTIVE</Badge>
          </div>
          <CardTitle>Prompt Amplifier Agent</CardTitle>
          <p class="agent-subtitle">Developer Enablement</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Enhances prompts from junior developers</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Adds missing context and best practices</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Suggests clearer technical requirements</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Guides developers to write better prompts</span>
            </li>
          </ul>
          <Button variant="default" class="demo-button purple" @click="openPromptAmplifierDialog">
            View Demo →
          </Button>
        </CardContent>
      </Card>
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
      showPromptAmplifierDialog: false
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
    viewDemo(agentType) {
      if (agentType === 'integration') {
        this.openIntegrationDialog()
      } else if (agentType === 'template') {
        this.openCodeTemplateDialog()
      } else if (agentType === 'prompt') {
        this.openPromptAmplifierDialog()
      } else {
        // Navigate to agent demo page for other agents
        this.$router.push(`/agent-hub/${agentType}`)
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
  align-items: flex-start;
  margin-bottom: 1rem;
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

.status-badge {
  background-color: #10b981;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
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
</style>
