<template>
  <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-6xl max-h-[90vh] border-0 flex flex-col p-0">
      <!-- Header - Fixed -->
      <div class="dialog-header-gradient">
        <div class="dialog-header-content">
          <div class="flex items-center gap-3">
            <div class="header-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
            </div>
            <div>
              <DialogTitle class="header-title">Prompt Amplifier Agent</DialogTitle>
              <p class="header-subtitle">Transforming Junior Prompts into Expert-Level Instructions</p>
            </div>
          </div>
          <DialogClose class="close-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </DialogClose>
        </div>
      </div>

      <!-- Scrollable Content -->
      <div class="dialog-body">
        <!-- Impact Metrics Section -->
        <div class="metrics-section">
          <div class="section-header-with-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <h3 class="section-title">Impact Metrics</h3>
          </div>
          <div class="metrics-grid">
            <Card class="metric-card">
              <CardContent>
                <div class="metric-icon-wrapper">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="6"></circle>
                    <circle cx="12" cy="12" r="2"></circle>
                  </svg>
                </div>
                <div class="metric-value">94%</div>
                <div class="metric-label">Success Rate</div>
                <div class="metric-description">First-time code generation success</div>
                <div class="metric-change positive">+12%</div>
              </CardContent>
            </Card>

            <Card class="metric-card">
              <CardContent>
                <div class="metric-icon-wrapper">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                </div>
                <div class="metric-value">3.2 hrs</div>
                <div class="metric-label">Time Saved</div>
                <div class="metric-description">Average per developer per day</div>
                <div class="metric-change positive">+45%</div>
              </CardContent>
            </Card>

            <Card class="metric-card">
              <CardContent>
                <div class="metric-icon-wrapper">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
                    <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
                  </svg>
                </div>
                <div class="metric-value">1,247</div>
                <div class="metric-label">Prompts Enhanced</div>
                <div class="metric-description">This month</div>
                <div class="metric-change positive">+28%</div>
              </CardContent>
            </Card>

            <Card class="metric-card">
              <CardContent>
                <div class="metric-icon-wrapper">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
                    <polyline points="16 18 22 12 16 6"></polyline>
                    <polyline points="8 6 2 12 8 18"></polyline>
                  </svg>
                </div>
                <div class="metric-value">87/100</div>
                <div class="metric-label">Code Quality</div>
                <div class="metric-description">Average quality score</div>
                <div class="metric-change positive">+15pts</div>
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- How It Works Section -->
        <div class="how-it-works-section">
          <h3 class="section-title">How It Works</h3>
          <div class="steps-grid">
            <div class="step-item">
              <div class="step-icon blue">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
              </div>
              <div class="step-number">STEP 1</div>
              <div class="step-title">Analyze Input</div>
              <div class="step-description">Parse the developer's prompt and identify missing context</div>
            </div>

            <div class="step-item">
              <div class="step-icon purple">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                  <path d="M6.5 2H20v20H6.5A2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                  <path d="M8 7h8M8 11h8M8 15h4"></path>
                </svg>
              </div>
              <div class="step-number">STEP 2</div>
              <div class="step-title">Query Knowledge Base</div>
              <div class="step-description">Pull relevant patterns, standards, and best practices</div>
            </div>

            <div class="step-item">
              <div class="step-icon pink">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
                </svg>
              </div>
              <div class="step-number">STEP 3</div>
              <div class="step-title">Amplify Context</div>
              <div class="step-description">Add technical specs, security requirements, and compliance rules</div>
            </div>

            <div class="step-item">
              <div class="step-icon orange">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
                </svg>
              </div>
              <div class="step-number">STEP 4</div>
              <div class="step-title">Generate Output</div>
              <div class="step-description">Produce comprehensive, production-ready prompt</div>
            </div>
          </div>
        </div>

        <!-- Amplify Your Own Prompt Section -->
        <div class="amplify-section">
          <h3 class="section-title">Amplify Your Own Prompt</h3>
          <div class="amplify-grid">
            <!-- Enter Your Prompt -->
            <Card class="amplify-panel">
              <CardHeader>
                <CardTitle class="panel-title">Enter Your Prompt</CardTitle>
              </CardHeader>
              <CardContent>
                <Textarea 
                  v-model="userPrompt" 
                  placeholder="Type your prompt here..."
                  rows="12"
                  class="prompt-textarea"
                />
                <Button variant="default" class="amplify-button" @click="amplifyPrompt" :disabled="loading">
                  {{ loading ? 'Amplifying...' : 'Amplify' }}
                </Button>
              </CardContent>
            </Card>

            <!-- Amplified Output -->
            <Card class="amplify-panel">
              <CardHeader>
                <div class="panel-header-with-action">
                  <CardTitle class="panel-title">Amplified Output</CardTitle>
                  <Button 
                    v-if="amplifiedOutput" 
                    variant="outline" 
                    size="sm" 
                    @click="copyEnhancedPrompt"
                    class="copy-prompt-button"
                    :class="{ 'copy-success': copySuccess }"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    {{ copySuccess ? 'Copied!' : 'Copy' }}
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div class="output-display">
                  <p v-if="!amplifiedOutput" class="output-placeholder">
                    Amplified prompt will appear here
                  </p>
                  <div v-else class="output-content">
                    <pre class="output-text">{{ amplifiedOutput }}</pre>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- Improvement Breakdown Section -->
        <div v-if="enhancedData && enhancedData.improvements && enhancedData.improvements.length > 0" class="improvement-breakdown-section">
          <h3 class="section-title">Improvement Breakdown</h3>
          <p class="section-subtitle">See what was enhanced in your prompt</p>
          <TooltipProvider>
            <div class="improvements-grid">
              <Tooltip 
                v-for="(improvement, index) in enhancedData.improvements" 
                :key="index"
              >
                <TooltipTrigger as-child>
                  <div class="improvement-card">
                    <div class="improvement-header">
                      <div class="improvement-icon-wrapper" :class="getImprovementTypeClass(improvement.type)">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="improvement-icon">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                      <div class="improvement-content">
                        <div class="improvement-type-badge" :class="getImprovementTypeClass(improvement.type)">
                          {{ getImprovementTypeLabel(improvement.type) }}
                        </div>
                        <div class="improvement-description-short">{{ improvement.description }}</div>
                      </div>
                    </div>
                  </div>
                </TooltipTrigger>
                <TooltipContent v-if="improvement.reason" class="improvement-tooltip">
                  <div class="tooltip-content">
                    <strong>Why this matters:</strong>
                    <p>{{ improvement.reason }}</p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </div>
          </TooltipProvider>
        </div>

        <!-- Knowledge Sources Used Section -->
        <div v-if="knowledgeSourcesUsed.length > 0" class="knowledge-sources-section">
          <h3 class="section-title">Knowledge Sources Used</h3>
          <div class="sources-used-grid">
            <Card 
              v-for="(source, index) in knowledgeSourcesUsed" 
              :key="index"
              class="source-card"
            >
              <CardContent>
                <div class="source-card-content">
                  <div class="source-icon-wrapper">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="source-icon">
                      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                    </svg>
                  </div>
                  <div class="source-details">
                    <div class="source-name-used">{{ source.source }}</div>
                    <div class="source-description-used">{{ source.description }}</div>
                  </div>
                  <Badge :variant="getSourceTypeVariant(source.type)" class="source-type-badge">
                    {{ getSourceTypeLabel(source.type) }}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- Agent Configuration Section -->
        <div class="configuration-section">
          <h3 class="section-title">Agent Configuration</h3>
          <div class="configuration-grid">
            <!-- Enhancement Rules -->
            <Card class="config-panel">
              <CardHeader>
                <CardTitle class="panel-title">Enhancement Rules</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="rules-list">
                  <div 
                    v-for="rule in enhancementRules" 
                    :key="rule.id"
                    class="rule-item"
                  >
                    <label class="rule-label">
                      <input 
                        type="checkbox" 
                        v-model="rule.enabled"
                        class="rule-checkbox"
                      />
                      <span class="rule-text">{{ rule.text }}</span>
                    </label>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- Knowledge Sources -->
            <Card class="config-panel">
              <CardHeader>
                <CardTitle class="panel-title">Knowledge Sources</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="sources-list">
                  <div 
                    v-for="source in knowledgeSources" 
                    :key="source.id"
                    class="source-item"
                  >
                    <div class="source-info">
                      <div class="source-name">{{ source.name }}</div>
                      <div class="source-docs">{{ source.docCount }} documents indexed</div>
                    </div>
                    <Badge :variant="getStatusVariant(source.status)" class="source-status">
                      {{ source.status }}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

    </DialogContent>
  </Dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { Dialog, DialogContent, DialogTitle, DialogClose } from './ui/dialog'
import { Button } from './ui/button'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Badge } from './ui/badge'
import { Textarea } from './ui/textarea'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip'

export default {
  name: 'PromptAmplifierAgentDialog',
  components: {
    Dialog,
    DialogContent,
    DialogTitle,
    DialogClose,
    Button,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Badge,
    Textarea,
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:open'],
  data() {
    return {
      userPrompt: '',
      amplifiedOutput: '',
      loading: false,
      copySuccess: false,
      enhancedData: null,
      knowledgeSourcesUsed: [],
      enhancementRules: [
        { id: 1, text: 'Always add security requirements', enabled: true },
        { id: 2, text: 'Include Axis Bank naming conventions', enabled: true },
        { id: 3, text: 'Suggest performance optimization', enabled: true },
        { id: 4, text: 'Add testing requirements (>80% coverage)', enabled: true },
        { id: 5, text: 'Reference internal design patterns', enabled: false }
      ],
      knowledgeSources: [
        { id: 1, name: 'Axis Bank Architecture Standards', docCount: 247, status: 'connected' },
        { id: 2, name: 'Internal Microservice Templates', docCount: 89, status: 'connected' },
        { id: 3, name: 'Security & Compliance Policies', docCount: 156, status: 'connected' },
        { id: 4, name: 'Best Practices Repository', docCount: 412, status: 'syncing' }
      ]
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjects', 'createProject']),
    ...mapActions('agents', ['runAgent']),
    async amplifyPrompt() {
      if (!this.userPrompt.trim()) {
        alert('Please enter a prompt to amplify')
        return
      }
      
      this.loading = true
      try {
        const projects = await this.fetchProjects()
        let projectId = projects && projects.length > 0 ? projects[0].id : null
        
        if (!projectId) {
          const newProject = await this.createProject({
            name: 'Prompt Amplifier Agent Demo',
            description: 'Demo project for Prompt Amplifier Agent'
          })
          projectId = newProject.id
        }
        
        const enabledRules = this.enhancementRules.filter(r => r.enabled).map(r => r.text)
        const context = `Enhancement Rules Enabled:\n${enabledRules.join('\n')}`
        
        const result = await this.runAgent({
          agentType: 'prompt_amplifier_agent',
          request: {
            project_id: projectId,
            original_prompt: this.userPrompt,
            context: context,
            agent_config: {
              temperature: 0.2,
              max_tokens: 2000
            },
            enhancement_rules: this.enhancementRules
          }
        })
        
        if (result.status === 'success' && result.enhanced) {
          this.amplifiedOutput = result.enhanced.enhanced_prompt || result.enhanced.original_prompt
          this.enhancedData = result.enhanced
          this.knowledgeSourcesUsed = result.enhanced.knowledge_sources_used || []
        } else {
          alert('Failed to amplify prompt: ' + (result.error || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error amplifying prompt:', error)
        alert('Failed to amplify prompt: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loading = false
      }
    },
    getStatusVariant(status) {
      if (status === 'connected') return 'default'
      if (status === 'syncing') return 'secondary'
      return 'outline'
    },
    async copyEnhancedPrompt() {
      if (!this.amplifiedOutput) {
        return
      }
      
      const promptText = this.amplifiedOutput
      
      // Try modern Clipboard API first
      if (navigator.clipboard && navigator.clipboard.writeText) {
        try {
          await navigator.clipboard.writeText(promptText)
          this.copySuccess = true
          setTimeout(() => {
            this.copySuccess = false
          }, 2000)
          return
        } catch (err) {
          console.error('Clipboard API failed:', err)
        }
      }
      
      // Fallback method
      try {
        const textarea = document.createElement('textarea')
        textarea.value = promptText
        textarea.style.position = 'fixed'
        textarea.style.left = '-9999px'
        textarea.style.top = '0'
        textarea.setAttribute('readonly', '')
        document.body.appendChild(textarea)
        
        if (navigator.userAgent.match(/ipad|iphone/i)) {
          const range = document.createRange()
          range.selectNodeContents(textarea)
          const selection = window.getSelection()
          selection.removeAllRanges()
          selection.addRange(range)
          textarea.setSelectionRange(0, 999999)
        } else {
          textarea.select()
          textarea.setSelectionRange(0, promptText.length)
        }
        
        const successful = document.execCommand('copy')
        document.body.removeChild(textarea)
        
        if (successful) {
          this.copySuccess = true
          setTimeout(() => {
            this.copySuccess = false
          }, 2000)
        } else {
          alert('Failed to copy to clipboard. Please copy manually.')
        }
      } catch (err) {
        console.error('Copy failed:', err)
        alert('Failed to copy to clipboard. Please copy manually.')
      }
    },
    getSourceTypeVariant(type) {
      const variants = {
        'codebase': 'default',
        'user_context': 'secondary',
        'security_policies': 'destructive',
        'architecture_standards': 'default',
        'best_practices': 'secondary',
        'design_patterns': 'outline',
        'ai_knowledge': 'outline'
      }
      return variants[type] || 'outline'
    },
    getSourceTypeLabel(type) {
      const labels = {
        'codebase': 'Codebase',
        'user_context': 'User Context',
        'security_policies': 'Security',
        'architecture_standards': 'Architecture',
        'best_practices': 'Best Practices',
        'design_patterns': 'Design Patterns',
        'ai_knowledge': 'AI Knowledge'
      }
      return labels[type] || 'Other'
    },
    getImprovementTypeClass(type) {
      const classes = {
        'context': 'type-context',
        'requirements': 'type-requirements',
        'best_practices': 'type-best-practices',
        'edge_cases': 'type-edge-cases',
        'error_handling': 'type-error-handling',
        'performance': 'type-performance',
        'security': 'type-security'
      }
      return classes[type] || 'type-default'
    },
    getImprovementTypeLabel(type) {
      const labels = {
        'context': 'Context Added',
        'requirements': 'Requirements',
        'best_practices': 'Best Practices',
        'edge_cases': 'Edge Cases',
        'error_handling': 'Error Handling',
        'performance': 'Performance',
        'security': 'Security'
      }
      return labels[type] || 'Improvement'
    }
  }
}
</script>

<style scoped>
.dialog-header-gradient {
  background: linear-gradient(135deg, #97144D 0%, #7a0f3d 100%);
  color: white;
  padding: 2rem;
  margin: 0;
  position: sticky;
  top: 0;
  z-index: 1001;
  flex-shrink: 0;
}

.dialog-header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.25rem;
}

.header-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: white;
  border-radius: 4px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.dialog-body {
  padding: 2rem;
  background: #f5f5f5;
  margin: 0;
  overflow-y: auto;
  flex: 1;
}

.section-header-with-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

/* Impact Metrics */
.metrics-section {
  margin-bottom: 3rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.metric-card {
  background: white;
  border: 1px solid #e5e5e5;
}

.metric-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #f3e8ff;
  color: #97144D;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.metric-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

/* How It Works */
.how-it-works-section {
  margin-bottom: 3rem;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.step-item {
  text-align: center;
}

.step-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.step-icon.blue {
  background-color: #dbeafe;
  color: #3b82f6;
}

.step-icon.purple {
  background-color: #f3e8ff;
  color: #97144D;
}

.step-icon.pink {
  background-color: #fce7f3;
  color: #ec4899;
}

.step-icon.orange {
  background-color: #fed7aa;
  color: #f97316;
}

.step-number {
  font-size: 0.75rem;
  font-weight: 600;
  color: #97144D;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.step-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.step-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

/* Amplify Section */
.amplify-section {
  margin-bottom: 3rem;
}

.amplify-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.amplify-panel {
  background: white;
  border: 1px solid #e5e5e5;
}

.panel-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.panel-header-with-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.copy-prompt-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-color: #97144D;
  color: #97144D;
  background-color: white;
}

.copy-prompt-button:hover {
  background-color: #97144D;
  color: white;
  border-color: #97144D;
}

.copy-prompt-button.copy-success {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.prompt-textarea {
  width: 100%;
  min-height: 200px;
  padding: 1rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  font-size: 0.875rem;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 1rem;
}

.prompt-textarea:focus {
  outline: none;
  border-color: #97144D;
}

.amplify-button {
  background-color: #97144D;
  color: white;
  border: none;
  width: 100%;
  padding: 0.75rem;
  font-weight: 600;
}

.amplify-button:hover {
  background-color: #7a0f3d;
}

.output-display {
  min-height: 200px;
  padding: 1rem;
  background-color: #f9fafb;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
}

.output-placeholder {
  color: #9ca3af;
  font-style: italic;
  text-align: center;
  margin: 0;
  padding: 2rem 0;
}

.output-content {
  width: 100%;
}

.output-text {
  font-size: 0.875rem;
  color: #374151;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: inherit;
}

/* Improvement Breakdown Section */
.improvement-breakdown-section {
  margin-bottom: 2rem;
}

.section-subtitle {
  font-size: 0.8125rem;
  color: #6b7280;
  margin-top: 0.25rem;
  margin-bottom: 1rem;
}

.improvements-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

@media (max-width: 1024px) {
  .improvements-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .improvements-grid {
    grid-template-columns: 1fr;
  }
}

.improvement-card {
  background: #f9fafb;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  transition: all 0.2s;
  overflow: hidden;
  cursor: help;
}

.improvement-card:hover {
  border-color: #97144D;
  box-shadow: 0 1px 4px rgba(151, 20, 77, 0.08);
}

.improvement-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
}

.improvement-icon-wrapper {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.improvement-icon-wrapper.type-context {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.improvement-icon-wrapper.type-requirements {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.improvement-icon-wrapper.type-best-practices {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.improvement-icon-wrapper.type-edge-cases {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.improvement-icon-wrapper.type-error-handling {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.improvement-icon-wrapper.type-performance {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
}

.improvement-icon-wrapper.type-security {
  background: linear-gradient(135deg, #97144D 0%, #7a0f3d 100%);
}

.improvement-icon-wrapper.type-default {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}

.improvement-icon {
  width: 16px;
  height: 16px;
}

.improvement-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.improvement-type-badge {
  display: inline-block;
  padding: 0.1875rem 0.625rem;
  border-radius: 10px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  width: fit-content;
}

.improvement-type-badge.type-context {
  background-color: #dbeafe;
  color: #1e40af;
}

.improvement-type-badge.type-requirements {
  background-color: #ede9fe;
  color: #5b21b6;
}

.improvement-type-badge.type-best-practices {
  background-color: #d1fae5;
  color: #065f46;
}

.improvement-type-badge.type-edge-cases {
  background-color: #fef3c7;
  color: #92400e;
}

.improvement-type-badge.type-error-handling {
  background-color: #fee2e2;
  color: #991b1b;
}

.improvement-type-badge.type-performance {
  background-color: #cffafe;
  color: #0e7490;
}

.improvement-type-badge.type-security {
  background-color: #fce7f3;
  color: #97144D;
}

.improvement-type-badge.type-default {
  background-color: #f3f4f6;
  color: #374151;
}

.improvement-description-short {
  font-size: 0.8125rem;
  font-weight: 400;
  color: #374151;
  line-height: 1.5;
  margin: 0;
}

.improvement-tooltip {
  max-width: 300px;
  z-index: 50;
}

.tooltip-content {
  padding: 0.5rem;
}

.tooltip-content strong {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.375rem;
}

.tooltip-content p {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

/* Knowledge Sources Used Section */
.knowledge-sources-section {
  margin-bottom: 3rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  border-radius: 12px;
  border: 1px solid #e5e5e5;
}

.sources-used-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.source-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.source-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #97144D;
}

.source-card-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.5rem 0;
}

.source-icon-wrapper {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #97144D 0%, #7a0f3d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.source-icon {
  width: 20px;
  height: 20px;
}

.source-details {
  flex: 1;
  min-width: 0;
}

.source-name-used {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.375rem;
  line-height: 1.4;
}

.source-description-used {
  font-size: 0.8125rem;
  color: #6b7280;
  line-height: 1.5;
}

.source-type-badge {
  flex-shrink: 0;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

/* Configuration Section */
.configuration-section {
  margin-bottom: 2rem;
}

.configuration-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.config-panel {
  background: white;
  border: 1px solid #e5e5e5;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rule-item {
  display: flex;
  align-items: center;
}

.rule-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  width: 100%;
}

.rule-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #97144D;
}

.rule-text {
  font-size: 0.875rem;
  color: #374151;
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.source-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: #f9fafb;
  border-radius: 6px;
}

.source-info {
  flex: 1;
}

.source-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.source-docs {
  font-size: 0.75rem;
  color: #6b7280;
}

.source-status {
  font-size: 0.75rem;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: white;
  border-top: 1px solid #e5e5e5;
}

.pro-tip {
  font-size: 0.875rem;
  color: #6b7280;
}

.pro-tip strong {
  color: #374151;
}

.close-footer-button {
  background-color: #97144D;
  color: white;
  border: none;
}

.close-footer-button:hover {
  background-color: #7a0f3d;
}

@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .steps-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .amplify-grid,
  .configuration-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .metrics-grid,
  .steps-grid {
    grid-template-columns: 1fr;
  }
  
  .dialog-body {
    padding: 1rem;
  }
  
  .dialog-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }
}
</style>
