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
          <Button variant="default" class="demo-button purple" @click="openCodeTemplateDialog">
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

      <!-- Test Data UI Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon teal">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="21" x2="9" y2="9"></line>
              </svg>
            </div>
          </div>
          <CardTitle>Test Data UI Agent</CardTitle>
          <p class="agent-subtitle">Testing Environment Control</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates intuitive UIs for test data creation</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Provides feature flag management interface</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Creates mock data generators for scenarios</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Enables real-time configuration changes</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Test Case Generator Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon red">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <line x1="8" y1="12" x2="16" y2="12"></line>
              </svg>
            </div>
          </div>
          <CardTitle>Test Case Generator Agent</CardTitle>
          <p class="agent-subtitle">Intelligent Test Coverage</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Analyzes code to suggest comprehensive test cases</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates edge case and boundary tests</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Creates regression test suites automatically</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Identifies untested code paths</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Load Testing Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon orange">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
          </div>
          <CardTitle>Load Testing Agent</CardTitle>
          <p class="agent-subtitle">Performance Validation</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Simulates realistic load scenarios</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Identifies performance bottlenecks</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates scalability recommendations</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Auto-tunes resource configurations</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- DevOps Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon orange">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
              </svg>
            </div>
          </div>
          <CardTitle>DevOps Agent</CardTitle>
          <p class="agent-subtitle">Automated Operations</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>CI/CD pipeline configuration</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Auto-scaling and monitoring setup</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Performance optimization suggestions</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Automated rollback on failures</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Documentation Agent -->
      <Card class="agent-card">
        <CardHeader>
          <div class="agent-card-header">
            <div class="agent-icon blue">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                <path d="M8 7h8M8 11h8M8 15h4"></path>
              </svg>
            </div>
          </div>
          <CardTitle>Documentation Agent</CardTitle>
          <p class="agent-subtitle">Standardized Knowledge</p>
        </CardHeader>
        <CardContent>
          <ul class="features-list">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Auto-generates comprehensive docs</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Creates diagrams and flowcharts</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Maintains changelog and versioning</span>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="check-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Generates onboarding guides</span>
            </li>
          </ul>
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
      }
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
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
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
