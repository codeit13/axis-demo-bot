<template>
  <div class="agent-run-output">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading agent run output...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>Error: {{ error }}</p>
      <Button @click="fetchSuggestion" variant="default">Retry</Button>
    </div>

    <!-- Content -->
    <template v-else-if="suggestion">
      <!-- Header -->
      <div class="output-header">
        <Button @click="$router.push('/')" variant="outline" class="back-button">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Back to Dashboard
        </Button>
        <div class="header-content">
          <div class="agent-info">
            <div class="agent-icon" :class="getAgentIconClass(suggestion.agent_type)">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
            </div>
            <div>
              <h1 class="agent-title">{{ formatAgentType(suggestion.agent_type) }}</h1>
              <p class="agent-subtitle">Agent Run Output</p>
            </div>
          </div>
          <Badge :variant="getStatusVariant(suggestion.status)" class="status-badge">
            {{ suggestion.status.toUpperCase() }}
          </Badge>
        </div>
      </div>

      <!-- Metadata -->
      <Card class="metadata-card">
        <CardContent>
          <div class="metadata-grid">
            <div class="metadata-item">
              <span class="metadata-label">Project ID:</span>
              <span class="metadata-value">{{ suggestion.project_id }}</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Created:</span>
              <span class="metadata-value">{{ formatDate(suggestion.created_at) }}</span>
            </div>
            <div class="metadata-item" v-if="suggestion.code_file_id">
              <span class="metadata-label">Code File ID:</span>
              <span class="metadata-value">{{ suggestion.code_file_id }}</span>
            </div>
            <div class="metadata-item" v-if="suggestion.issue_id">
              <span class="metadata-label">Issue ID:</span>
              <span class="metadata-value">{{ suggestion.issue_id }}</span>
            </div>
            <div class="metadata-item" v-if="suggestion.rule_id">
              <span class="metadata-label">Rule ID:</span>
              <span class="metadata-value">{{ suggestion.rule_id }}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Prompt Amplifier Agent Special UI -->
      <template v-if="isPromptAmplifierAgent">
        <!-- Amplified Output Section -->
        <Card class="output-card">
          <CardHeader>
            <div class="panel-header-with-action">
              <CardTitle>Amplified Output</CardTitle>
              <Button 
                v-if="amplifiedPrompt" 
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
              <p v-if="!amplifiedPrompt" class="output-placeholder">
                No amplified prompt available
              </p>
              <div v-else class="output-content">
                <pre class="output-text">{{ amplifiedPrompt }}</pre>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Improvement Breakdown Section -->
        <Card v-if="enhancedData && enhancedData.improvements && enhancedData.improvements.length > 0" class="output-card">
          <CardHeader>
            <CardTitle>Improvement Breakdown</CardTitle>
            <p class="section-subtitle">See what was enhanced in your prompt</p>
          </CardHeader>
          <CardContent>
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
          </CardContent>
        </Card>

        <!-- Knowledge Sources Used Section -->
        <Card v-if="knowledgeSourcesUsed.length > 0" class="output-card">
          <CardHeader>
            <CardTitle>Knowledge Sources Used</CardTitle>
          </CardHeader>
          <CardContent>
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
                      <div class="source-name-used">{{ source.source || source.name }}</div>
                      <div class="source-description-used">{{ source.description }}</div>
                    </div>
                    <Badge :variant="getSourceTypeVariant(source.type)" class="source-type-badge">
                      {{ getSourceTypeLabel(source.type) }}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>
      </template>

      <!-- Standard Output Content (for other agents) -->
      <Card v-else class="output-card">
        <CardHeader>
          <CardTitle>Agent Output</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="output-content">
            <!-- Try to parse and display structured content -->
            <div v-if="parsedContent" class="structured-output">
              <!-- Display parsed content based on agent type -->
              <div v-for="(value, key) in parsedContent" :key="key" class="output-section">
                <h3 class="section-title">{{ formatKey(key) }}</h3>
                <div class="section-content">
                  <pre v-if="isCodeBlock(key, value)" class="code-block">{{ formatValue(value) }}</pre>
                  <div v-else-if="Array.isArray(value)" class="array-content">
                    <div v-for="(item, index) in value" :key="index" class="array-item">
                      <div v-if="typeof item === 'object'" class="object-item">
                        <div v-for="(v, k) in item" :key="k" class="object-field">
                          <strong>{{ formatKey(k) }}:</strong>
                          <span>{{ formatValue(v) }}</span>
                        </div>
                      </div>
                      <div v-else class="simple-item">{{ formatValue(item) }}</div>
                    </div>
                  </div>
                  <div v-else-if="typeof value === 'object'" class="object-content">
                    <div v-for="(v, k) in value" :key="k" class="object-field">
                      <strong>{{ formatKey(k) }}:</strong>
                      <span>{{ formatValue(v) }}</span>
                    </div>
                  </div>
                  <p v-else class="text-content">{{ formatValue(value) }}</p>
                </div>
              </div>
            </div>
            <!-- Fallback to raw content display -->
            <div v-else class="raw-output">
              <pre class="code-block">{{ formatContent(suggestion.content) }}</pre>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- OpenAPI Spec Section (for Integration Agent) -->
      <Card v-if="isIntegrationAgent && openApiSpec" class="openapi-spec-card">
        <CardHeader>
          <div class="openapi-header">
            <CardTitle>OpenAPI 3.0 Specification</CardTitle>
            <div class="openapi-actions">
              <Button variant="outline" size="sm" @click="exportYAML" class="export-yaml-button">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Export YAML
              </Button>
              <Button variant="default" size="sm" @click="exportPDF" class="export-pdf-button">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                Export PDF
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div class="openapi-spec-container">
            <pre class="openapi-spec-content" ref="openapiSpecRef">{{ openApiSpec }}</pre>
          </div>
        </CardContent>
      </Card>

      <!-- Action Buttons (if pending) -->
      <div v-if="suggestion.status === 'pending'" class="action-buttons">
        <Button 
          @click="approveSuggestion" 
          variant="default" 
          class="approve-button"
          :disabled="processing"
        >
          ✓ Approve
        </Button>
        <Button 
          @click="rejectSuggestion" 
          variant="destructive"
          :disabled="processing"
        >
          ✗ Reject
        </Button>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import api from '../services/api'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip'

export default {
  name: 'AgentRunOutput',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Badge,
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
  },
  data() {
    return {
      loading: true,
      error: null,
      suggestion: null,
      processing: false,
      copySuccess: false
    }
  },
  computed: {
    parsedContent() {
      if (!this.suggestion || !this.suggestion.content) return null
      try {
        const parsed = JSON.parse(this.suggestion.content)
        // For prompt amplifier, exclude enhanced_prompt from parsedContent as it's displayed separately
        if (this.isPromptAmplifierAgent && parsed.enhanced_prompt) {
          const { enhanced_prompt, ...rest } = parsed
          return rest
        }
        // For integration agent, exclude openapi_spec from parsedContent as it's displayed separately
        if (this.isIntegrationAgent && parsed.openapi_spec) {
          const { openapi_spec, ...rest } = parsed
          return rest
        }
        return parsed
      } catch (e) {
        return null
      }
    },
    isPromptAmplifierAgent() {
      return this.suggestion && this.suggestion.agent_type === 'prompt_amplifier_agent'
    },
    isIntegrationAgent() {
      return this.suggestion && this.suggestion.agent_type === 'integration_agent'
    },
    amplifiedPrompt() {
      if (!this.isPromptAmplifierAgent || !this.parsedContent) return null
      try {
        const fullContent = JSON.parse(this.suggestion.content)
        return fullContent.enhanced_prompt || fullContent.enhanced?.enhanced_prompt || null
      } catch (e) {
        return null
      }
    },
    enhancedData() {
      if (!this.isPromptAmplifierAgent || !this.suggestion || !this.suggestion.content) return null
      try {
        const fullContent = JSON.parse(this.suggestion.content)
        return fullContent.enhanced || fullContent.improvements ? fullContent : null
      } catch (e) {
        return null
      }
    },
    knowledgeSourcesUsed() {
      if (!this.enhancedData) return []
      return this.enhancedData.knowledge_sources_used || []
    },
    openApiSpec() {
      if (!this.isIntegrationAgent || !this.parsedContent) return null
      try {
        const fullContent = JSON.parse(this.suggestion.content)
        let spec = fullContent.openapi_spec || fullContent.spec?.openapi_spec || null
        if (spec && typeof spec === 'string') {
          // Remove markdown code block markers if present
          spec = spec.replace(/^```yaml\s*/i, '').replace(/^```\s*/i, '').replace(/```\s*$/i, '').trim()
        }
        return spec
      } catch (e) {
        return null
      }
    }
  },
  mounted() {
    const suggestionId = this.$route.params.id
    if (suggestionId) {
      this.fetchSuggestion(suggestionId)
    } else {
      this.error = 'No suggestion ID provided'
      this.loading = false
    }
  },
  methods: {
    ...mapActions('suggestions', ['approveSuggestion']),
    async fetchSuggestion(suggestionId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.getSuggestion(suggestionId)
        this.suggestion = response.data
      } catch (error) {
        console.error('Error fetching suggestion:', error)
        this.error = error.response?.data?.detail || error.message || 'Failed to load suggestion'
      } finally {
        this.loading = false
      }
    },
    async approveSuggestion() {
      if (!this.suggestion) return
      this.processing = true
      try {
        await this.$store.dispatch('suggestions/approveSuggestion', {
          suggestionId: this.suggestion.id,
          action: 'approve',
          comments: 'Approved from agent run output view'
        })
        // Refresh suggestion to get updated status
        await this.fetchSuggestion(this.suggestion.id)
        alert('Suggestion approved successfully!')
      } catch (error) {
        alert('Failed to approve suggestion: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.processing = false
      }
    },
    async rejectSuggestion() {
      if (!this.suggestion) return
      const reason = prompt('Reason for rejection (optional):')
      this.processing = true
      try {
        await this.$store.dispatch('suggestions/approveSuggestion', {
          suggestionId: this.suggestion.id,
          action: 'reject',
          comments: reason || 'Rejected from agent run output view'
        })
        // Refresh suggestion to get updated status
        await this.fetchSuggestion(this.suggestion.id)
        alert('Suggestion rejected.')
      } catch (error) {
        alert('Failed to reject suggestion: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.processing = false
      }
    },
    formatAgentType(type) {
      return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    },
    formatKey(key) {
      return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    formatValue(value) {
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
      }
      return String(value)
    },
    formatContent(content) {
      try {
        const parsed = JSON.parse(content)
        return JSON.stringify(parsed, null, 2)
      } catch (e) {
        return content
      }
    },
    isCodeBlock(key, value) {
      const codeKeys = ['code', 'test_code', 'implementation', 'spec', 'yaml', 'openapi_spec']
      return codeKeys.some(k => key.toLowerCase().includes(k)) || 
             (typeof value === 'string' && value.length > 100 && 
              (value.includes('def ') || value.includes('function ') || value.includes('class ') || value.includes('import ')))
    },
    getAgentIconClass(agentType) {
      const classes = {
        'business_logic_policy': 'purple',
        'product_requirements': 'blue',
        'api_contract': 'green',
        'technical_architecture': 'orange',
        'quality_test': 'red',
        'change_impact': 'yellow',
        'release_readiness': 'pink'
      }
      return classes[agentType] || 'default'
    },
    getStatusVariant(status) {
      if (status === 'approved') return 'default'
      if (status === 'rejected') return 'destructive'
      return 'secondary'
    },
    async copyEnhancedPrompt() {
      if (!this.amplifiedPrompt) return
      
      const promptText = this.amplifiedPrompt
      
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
        }
      } catch (err) {
        console.error('Copy failed:', err)
        alert('Failed to copy to clipboard')
      }
    },
    getImprovementTypeClass(type) {
      const typeMap = {
        'security': 'security',
        'performance': 'performance',
        'testing': 'testing',
        'architecture': 'architecture',
        'compliance': 'compliance',
        'documentation': 'documentation'
      }
      return typeMap[type?.toLowerCase()] || 'default'
    },
    getImprovementTypeLabel(type) {
      const labelMap = {
        'security': 'Security',
        'performance': 'Performance',
        'testing': 'Testing',
        'architecture': 'Architecture',
        'compliance': 'Compliance',
        'documentation': 'Documentation'
      }
      return labelMap[type?.toLowerCase()] || 'Enhancement'
    },
    getSourceTypeVariant(type) {
      const variantMap = {
        'internal': 'default',
        'external': 'secondary',
        'documentation': 'outline'
      }
      return variantMap[type?.toLowerCase()] || 'default'
    },
    getSourceTypeLabel(type) {
      const labelMap = {
        'internal': 'Internal',
        'external': 'External',
        'documentation': 'Documentation'
      }
      return labelMap[type?.toLowerCase()] || 'Source'
    },
    exportYAML() {
      if (!this.openApiSpec) {
        alert('No OpenAPI specification available to export')
        return
      }
      
      let specText = this.openApiSpec
      
      // If it's a JSON string (escaped), unescape it
      if (specText.startsWith('"') && specText.endsWith('"')) {
        try {
          specText = JSON.parse(specText)
        } catch (e) {
          // Not a JSON string, use as is
        }
      }
      
      // Remove any markdown code block markers if present
      specText = specText.replace(/^```yaml\s*/i, '').replace(/^```\s*/i, '').replace(/```\s*$/i, '').trim()
      
      if (!specText || specText.length === 0) {
        alert('OpenAPI specification is empty')
        return
      }
      
      // Create and download YAML file
      const blob = new Blob([specText], { type: 'text/yaml;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      const serviceName = this.parsedContent?.serviceName || this.parsedContent?.service_name || 'API_Spec'
      a.download = `${serviceName.replace(/\s+/g, '_')}_API_Spec.yaml`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
    async exportPDF() {
      if (!this.openApiSpec) {
        alert('No OpenAPI specification available to export')
        return
      }
      
      try {
        // Dynamic import of jsPDF
        const { jsPDF } = await import('jspdf')
        
        const doc = new jsPDF()
        const pageWidth = doc.internal.pageSize.getWidth()
        const pageHeight = doc.internal.pageSize.getHeight()
        const margin = 20
        const maxWidth = pageWidth - 2 * margin
        let yPos = margin
        
        // Helper function to add a new page if needed
        const checkPageBreak = (requiredSpace = 10) => {
          if (yPos + requiredSpace > pageHeight - margin) {
            doc.addPage()
            yPos = margin
            return true
          }
          return false
        }
        
        // Helper function to add text with word wrap
        const addText = (text, fontSize, isBold = false, color = null) => {
          checkPageBreak(15)
          doc.setFontSize(fontSize)
          if (isBold) {
            doc.setFont(undefined, 'bold')
          } else {
            doc.setFont(undefined, 'normal')
          }
          if (color) {
            doc.setTextColor(color[0], color[1], color[2])
          }
          const lines = doc.splitTextToSize(text, maxWidth)
          for (let i = 0; i < lines.length; i++) {
            checkPageBreak(8)
            doc.text(lines[i], margin, yPos)
            yPos += fontSize * 0.5 + 2
          }
          if (color) {
            doc.setTextColor(0, 0, 0) // Reset to black
          }
        }
        
        // Get service information from parsed content
        const serviceName = this.parsedContent?.serviceName || this.parsedContent?.service_name || 'API Service'
        const version = this.parsedContent?.version || '1.0.0'
        const baseUrl = this.parsedContent?.baseUrl || this.parsedContent?.base_url || 'Not specified'
        const description = this.parsedContent?.description || 'No description provided'
        const authentication = this.parsedContent?.authentication || 'OAuth 2.0'
        const securityRequirements = this.parsedContent?.securityRequirements || this.parsedContent?.security_requirements || []
        const endpoints = this.parsedContent?.endpoints || []
        
        // Title
        addText(serviceName || 'API Specification', 20, true, [151, 20, 77])
        yPos += 5
        
        // Service Information Section
        addText('Service Information', 14, true)
        yPos += 3
        
        doc.setFontSize(10)
        doc.setFont(undefined, 'normal')
        addText(`Version: ${version}`, 10)
        addText(`Base URL: ${baseUrl}`, 10)
        addText(`Description: ${description}`, 10)
        addText(`Authentication: ${authentication}`, 10)
        yPos += 5
        
        // Security Requirements Section
        if (securityRequirements && securityRequirements.length > 0) {
          addText('Security Requirements', 14, true)
          yPos += 3
          doc.setFontSize(10)
          securityRequirements.forEach(req => {
            addText(`• ${req}`, 10)
          })
          yPos += 5
        }
        
        // Endpoints Section
        if (endpoints && endpoints.length > 0) {
          addText('API Endpoints', 14, true)
          yPos += 3
          
          endpoints.forEach((endpoint, index) => {
            checkPageBreak(25)
            
            // Endpoint header
            doc.setFontSize(12)
            doc.setFont(undefined, 'bold')
            const endpointTitle = `${endpoint.method || 'GET'} ${endpoint.path || '/endpoint'}`
            addText(endpointTitle, 12, true, [151, 20, 77])
            yPos += 2
            
            // Endpoint description
            if (endpoint.description || endpoint.summary) {
              doc.setFontSize(10)
              doc.setFont(undefined, 'normal')
              addText(endpoint.description || endpoint.summary, 10)
              yPos += 2
            }
            
            // Parameters
            if (endpoint.parameters && endpoint.parameters.length > 0) {
              doc.setFontSize(10)
              doc.setFont(undefined, 'bold')
              addText('Parameters:', 10, true)
              doc.setFont(undefined, 'normal')
              endpoint.parameters.forEach(param => {
                const paramText = `  • ${param.name || 'param'} (${param.in || 'query'}): ${param.description || 'No description'}`
                addText(paramText, 9)
              })
              yPos += 2
            }
            
            // Responses
            if (endpoint.responses) {
              doc.setFontSize(10)
              doc.setFont(undefined, 'bold')
              addText('Responses:', 10, true)
              doc.setFont(undefined, 'normal')
              Object.keys(endpoint.responses).forEach(statusCode => {
                const response = endpoint.responses[statusCode]
                const responseText = `  • ${statusCode}: ${response.description || 'No description'}`
                addText(responseText, 9)
              })
              yPos += 2
            }
            
            yPos += 3 // Space between endpoints
          })
        } else {
          // If no endpoints, add a note
          addText('API Endpoints', 14, true)
          yPos += 3
          addText('No endpoints defined. Please refer to the OpenAPI specification for complete endpoint details.', 10)
          yPos += 5
        }
        
        // OpenAPI Specification Reference
        addText('OpenAPI Specification', 14, true)
        yPos += 3
        addText('This API follows OpenAPI 3.0.0 specification standards. For the complete OpenAPI YAML specification, please refer to the generated OpenAPI spec that can be imported into Swagger Editor.', 10)
        yPos += 3
        addText('Swagger Editor: https://editor.swagger.io/', 10)
        
        // Footer
        const totalPages = doc.internal.getNumberOfPages()
        for (let i = 1; i <= totalPages; i++) {
          doc.setPage(i)
          doc.setFontSize(8)
          doc.setTextColor(128, 128, 128)
          doc.text(
            `Page ${i} of ${totalPages}`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
          )
          doc.text(
            `Generated on ${new Date().toLocaleDateString()}`,
            pageWidth - margin,
            pageHeight - 10,
            { align: 'right' }
          )
          doc.setTextColor(0, 0, 0)
        }
        
        // Save PDF
        const fileName = `${serviceName.replace(/\s+/g, '_')}_API_Documentation.pdf`
        doc.save(fileName)
      } catch (error) {
        console.error('Error exporting PDF:', error)
        alert('Failed to export PDF: ' + error.message)
      }
    }
  }
}
</script>

<style scoped>
.agent-run-output {
  padding: 2rem;
  max-width: 1200px;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f4f6;
  border-top-color: #97144D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.output-header {
  margin-bottom: 2rem;
}

.back-button {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1.25rem;
  font-size: 0.9375rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #e5e5e5;
  background-color: white;
  color: #374151;
  border-radius: 6px;
  transition: all 0.2s;
  cursor: pointer;
}

.back-button:hover {
  background-color: #f9fafb;
  border-color: #97144D;
  color: #97144D;
  box-shadow: 0 1px 3px rgba(151, 20, 77, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.agent-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.agent-icon.purple {
  background-color: #f3e8ff;
  color: #97144D;
}

.agent-icon.blue {
  background-color: #dbeafe;
  color: #3b82f6;
}

.agent-icon.green {
  background-color: #d1fae5;
  color: #10b981;
}

.agent-icon.orange {
  background-color: #fed7aa;
  color: #f97316;
}

.agent-icon.red {
  background-color: #fee2e2;
  color: #ef4444;
}

.agent-icon.yellow {
  background-color: #fef3c7;
  color: #f59e0b;
}

.agent-icon.pink {
  background-color: #fce7f3;
  color: #ec4899;
}

.agent-icon.default {
  background-color: #f3f4f6;
  color: #6b7280;
}

.agent-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.agent-subtitle {
  font-size: 1rem;
  color: #6b7280;
}

.status-badge {
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
}

.metadata-card {
  margin-bottom: 2rem;
}

.metadata-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.metadata-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metadata-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.metadata-value {
  font-size: 1rem;
  color: #1f2937;
  font-weight: 600;
}

.output-card {
  margin-bottom: 2rem;
}

.output-content {
  padding: 1rem 0;
}

.structured-output {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.output-section {
  border-bottom: 1px solid #e5e5e5;
  padding-bottom: 1.5rem;
}

.output-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-content {
  color: #374151;
}

.code-block {
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 0;
}

.text-content {
  font-size: 1rem;
  line-height: 1.6;
  white-space: pre-wrap;
}

.array-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.array-item {
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e5e5;
}

.object-content,
.object-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.object-field {
  display: flex;
  gap: 0.5rem;
}

.object-field strong {
  min-width: 150px;
  color: #374151;
}

.raw-output {
  padding: 1rem 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e5e5e5;
}

.approve-button {
  background-color: #10b981;
  color: white;
}

.approve-button:hover:not(:disabled) {
  background-color: #059669;
}

/* OpenAPI Spec Section */
.openapi-spec-card {
  margin-bottom: 2rem;
}

.openapi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.openapi-actions {
  display: flex;
  gap: 0.75rem;
}

.export-yaml-button,
.export-pdf-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-pdf-button {
  background-color: #97144D;
  color: white;
  border: none;
}

.export-pdf-button:hover {
  background-color: #7a0f3d;
}

.openapi-spec-container {
  height: 400px;
  overflow-y: auto;
  overflow-x: hidden;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #1e1e1e;
}

.openapi-spec-content {
  margin: 0;
  padding: 1.5rem;
  color: #d4d4d4;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Prompt Amplifier UI Styles */
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
  transition: all 0.2s;
}

.copy-prompt-button.copy-success {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.output-display {
  min-height: 200px;
}

.output-placeholder {
  color: #9ca3af;
  font-style: italic;
  padding: 2rem;
  text-align: center;
}

.output-text {
  background-color: #f9fafb;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 1.5rem;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  color: #374151;
}

.section-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

/* Improvement Breakdown */
.improvements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.improvement-card {
  padding: 1rem;
  background-color: #f9fafb;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.improvement-card:hover {
  border-color: #97144D;
  box-shadow: 0 2px 4px rgba(151, 20, 77, 0.1);
}

.improvement-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.improvement-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.improvement-icon-wrapper.security {
  background-color: #fee2e2;
  color: #ef4444;
}

.improvement-icon-wrapper.performance {
  background-color: #dbeafe;
  color: #3b82f6;
}

.improvement-icon-wrapper.testing {
  background-color: #d1fae5;
  color: #10b981;
}

.improvement-icon-wrapper.architecture {
  background-color: #f3e8ff;
  color: #97144D;
}

.improvement-icon-wrapper.compliance {
  background-color: #fef3c7;
  color: #f59e0b;
}

.improvement-icon-wrapper.documentation {
  background-color: #e0e7ff;
  color: #6366f1;
}

.improvement-icon-wrapper.default {
  background-color: #f3f4f6;
  color: #6b7280;
}

.improvement-content {
  flex: 1;
  min-width: 0;
}

.improvement-type-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.improvement-type-badge.security {
  background-color: #fee2e2;
  color: #991b1b;
}

.improvement-type-badge.performance {
  background-color: #dbeafe;
  color: #1e40af;
}

.improvement-type-badge.testing {
  background-color: #d1fae5;
  color: #065f46;
}

.improvement-type-badge.architecture {
  background-color: #f3e8ff;
  color: #6b21a8;
}

.improvement-type-badge.compliance {
  background-color: #fef3c7;
  color: #92400e;
}

.improvement-type-badge.documentation {
  background-color: #e0e7ff;
  color: #3730a3;
}

.improvement-type-badge.default {
  background-color: #f3f4f6;
  color: #374151;
}

.improvement-description-short {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
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
  margin-bottom: 0.25rem;
  color: #1f2937;
}

.tooltip-content p {
  margin: 0;
  color: #4b5563;
  font-size: 0.875rem;
}

/* Knowledge Sources Used */
.sources-used-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.source-card {
  border: 1px solid #e5e5e5;
}

.source-card-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.source-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #97144D;
}

.source-details {
  flex: 1;
  min-width: 0;
}

.source-name-used {
  font-weight: 600;
  font-size: 0.875rem;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.source-description-used {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.4;
}

.source-type-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

@media (max-width: 768px) {
  .agent-run-output {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .metadata-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .openapi-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .openapi-actions {
    width: 100%;
    flex-direction: column;
  }

  .openapi-actions .export-yaml-button,
  .openapi-actions .export-pdf-button {
    width: 100%;
    justify-content: center;
  }

  .improvements-grid,
  .sources-used-grid {
    grid-template-columns: 1fr;
  }
}
</style>
