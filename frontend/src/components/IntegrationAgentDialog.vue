<template>
  <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-4xl max-h-[90vh] border-0 flex flex-col p-0">
      <!-- Header - Fixed -->
      <div class="dialog-header-gradient">
        <div class="dialog-header-content">
          <div class="flex items-center gap-3">
            <div class="header-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="8" height="8" rx="2"></rect>
                <rect x="14" y="2" width="8" height="8" rx="2"></rect>
                <rect x="2" y="14" width="8" height="8" rx="2"></rect>
                <rect x="14" y="14" width="8" height="8" rx="2"></rect>
              </svg>
            </div>
            <div>
              <DialogTitle class="header-title">Integration Agent</DialogTitle>
              <p class="header-subtitle">Generate API Specifications in Standard Format</p>
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
      <!-- How It Works Section -->
      <div class="how-it-works-section">
        <h3 class="section-title">How It Works</h3>
        <div class="steps-grid">
          <div class="step-item">
            <div class="step-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <polyline points="9 9 12 12 15 9"></polyline>
              </svg>
            </div>
            <div class="step-number">STEP 1</div>
            <div class="step-title">Describe Service</div>
            <div class="step-description">Provide service details and base URL</div>
          </div>

          <div class="step-item">
            <div class="step-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>
            <div class="step-number">STEP 2</div>
            <div class="step-title">Define Endpoints</div>
            <div class="step-description">Specify API endpoints and parameters</div>
          </div>

          <div class="step-item">
            <div class="step-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
            </div>
            <div class="step-number">STEP 3</div>
            <div class="step-title">Generate Spec</div>
            <div class="step-description">AI creates OpenAPI 3.0 documentation</div>
          </div>

          <div class="step-item">
            <div class="step-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </div>
            <div class="step-number">STEP 4</div>
            <div class="step-title">Export as PDF</div>
            <div class="step-description">Share with frontend teams instantly</div>
          </div>
        </div>
      </div>

      <!-- Create API Specification Section -->
      <div class="create-spec-section">
        <div class="section-header">
          <h3 class="section-title">Create API Specification</h3>
          <Button variant="outline" class="load-sample-button" @click="loadSampleData">
            Load Sample Data
          </Button>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Service Name</label>
            <Input 
              v-model="formData.serviceName" 
              placeholder="e.g., Payment Processing Service"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Base URL</label>
            <Input 
              v-model="formData.baseUrl" 
              placeholder="e.g., https://api.axisbank.com/payments/v1"
              class="form-input"
            />
          </div>
        </div>

        <div class="form-group full-width">
          <label class="form-label">Service Description</label>
          <Textarea 
            v-model="formData.description" 
            placeholder="Describe what this service does..."
            rows="4"
            class="form-textarea"
          />
        </div>

        <div class="generate-button-container">
          <Button 
            variant="default" 
            class="generate-button" 
            @click="generateSpec"
            :disabled="loading"
          >
            <svg v-if="loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner">
              <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
              <path d="M12 2 A10 10 0 0 1 22 12" stroke-linecap="round"></path>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
            </svg>
            {{ loading ? 'Generating...' : 'Generate API Specification' }}
          </Button>
        </div>
      </div>

      <!-- Generated Specification Result -->
      <div v-if="specGenerated" class="spec-result-section">
        <Card class="spec-result-card">
          <CardContent class="spec-result-content">
            <div class="spec-header">
              <div class="spec-title-section">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" class="success-icon">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <div>
                  <h3 class="spec-result-title">API Specification Generated</h3>
                  <p class="spec-result-subtitle">Ready to export and share with frontend teams</p>
                </div>
              </div>
              <Button variant="default" size="sm" class="export-pdf-header-button" @click="exportPDF">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Export as PDF
              </Button>
            </div>

            <div class="spec-details">
              <!-- Service Name Section -->
              <div class="spec-section">
                <h4 class="spec-section-title">Service Name</h4>
                <div class="spec-info-grid">
                  <div class="spec-info-item">
                    <span class="spec-label">Version:</span>
                    <span class="spec-value">{{ generatedSpec.version || '1.0.0' }}</span>
                  </div>
                  <div class="spec-info-item">
                    <span class="spec-label">Base URL:</span>
                    <span class="spec-url-badge">{{ generatedSpec.baseUrl || formData.baseUrl || 'https://api.example.com/v1' }}</span>
                  </div>
                  <div class="spec-info-item full-width">
                    <span class="spec-label">Description:</span>
                    <span class="spec-value">{{ generatedSpec.description || formData.description || 'API service description' }}</span>
                  </div>
                  <div class="spec-info-item">
                    <span class="spec-label">Authentication:</span>
                    <span class="spec-value">{{ generatedSpec.authentication || 'OAuth 2.0' }}</span>
                  </div>
                </div>
              </div>

              <!-- Endpoints Section -->
              <div class="spec-section">
                <h4 class="spec-section-title">Endpoints</h4>
                <div v-if="generatedSpec.endpoints && generatedSpec.endpoints.length > 0" class="endpoints-list">
                  <div v-for="(endpoint, index) in generatedSpec.endpoints" :key="index" class="endpoint-item">
                    <div class="endpoint-method">{{ endpoint.method }}</div>
                    <div class="endpoint-path">{{ endpoint.path }}</div>
                    <div class="endpoint-description">{{ endpoint.description || endpoint.summary }}</div>
                  </div>
                </div>
                <div v-else class="endpoints-placeholder">
                  <p class="placeholder-text">No endpoints defined yet</p>
                </div>
              </div>

              <!-- Security Requirements Section -->
              <div class="spec-section">
                <h4 class="spec-section-title">Security Requirements</h4>
                <ul class="security-requirements">
                  <li v-for="(req, index) in generatedSpec.securityRequirements" :key="index">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span>{{ req }}</span>
                  </li>
                </ul>
              </div>

              <!-- OpenAPI 3.0 Spec Section -->
              <div class="spec-section">
                <div class="spec-section-header">
                  <h4 class="spec-section-title">OpenAPI 3.0 Specification</h4>
                  <div class="spec-actions">
                    <Button variant="outline" size="sm" @click="copyOpenAPISpec" class="copy-button">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                      </svg>
                      {{ copySuccess ? 'Copied!' : 'Copy' }}
                    </Button>
                    <Button variant="outline" size="sm" @click="exportYAML" class="export-yaml-button">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                      </svg>
                      Export YAML
                    </Button>
                  </div>
                </div>
                <div class="openapi-spec-box">
                  <pre class="openapi-spec-content" ref="openapiSpecRef">{{ generatedSpec.openapi_spec || 'OpenAPI specification will appear here...' }}</pre>
                </div>
                <p class="openapi-description">
                  This specification is fully compatible with Swagger Editor. Copy the YAML above and paste it directly into <a href="https://editor.swagger.io/" target="_blank" class="swagger-link">Swagger Editor</a> to view and test the API.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { Dialog, DialogContent, DialogTitle, DialogClose } from './ui/dialog'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Card, CardContent } from './ui/card'

export default {
  name: 'IntegrationAgentDialog',
  components: {
    Dialog,
    DialogContent,
    DialogTitle,
    DialogClose,
    Button,
    Input,
    Textarea,
    Card,
    CardContent
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
      specGenerated: false,
      loading: false,
      formData: {
        serviceName: '',
        baseUrl: '',
        description: ''
      },
      generatedSpec: {
        serviceName: '',
        version: '',
        baseUrl: '',
        description: '',
        authentication: 'OAuth 2.0',
        endpoints: [],
        securityRequirements: [],
        openapi_spec: ''
      },
      copySuccess: false
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjects', 'createProject']),
    ...mapActions('agents', ['runAgent']),
    loadSampleData() {
      this.formData = {
        serviceName: 'Payment Processing Service',
        baseUrl: 'https://api.axisbank.com/payments/v1',
        description: 'A comprehensive payment processing service that handles credit card transactions, bank transfers, and digital wallet payments. Supports multiple payment gateways and provides real-time transaction status updates.'
      }
    },
    async generateSpec() {
      if (!this.formData.serviceName && !this.formData.baseUrl && !this.formData.description) {
        alert('Please fill in at least one field or load sample data')
        return
      }
      
      this.loading = true
      try {
        // Get or create a default project (you may want to pass project_id as prop)
        const projects = await this.$store.dispatch('projects/fetchProjects')
        let projectId = projects && projects.length > 0 ? projects[0].id : null
        
        if (!projectId) {
          // Create a default project for demo purposes
          const newProject = await this.$store.dispatch('projects/createProject', {
            name: 'Integration Agent Demo',
            description: 'Demo project for Integration Agent'
          })
          projectId = newProject.id
        }
        
        // Call backend API
        const result = await this.$store.dispatch('agents/runAgent', {
          agentType: 'integration_agent',
          request: {
            project_id: projectId,
            service_name: this.formData.serviceName || 'API Service',
            base_url: this.formData.baseUrl || 'https://api.example.com/v1',
            description: this.formData.description || 'API service description'
          }
        })
        
        if (result.status === 'success' && result.spec) {
          this.generatedSpec = {
            serviceName: result.spec.serviceName || this.formData.serviceName,
            version: result.spec.version || '1.0.0',
            baseUrl: result.spec.baseUrl || this.formData.baseUrl,
            description: result.spec.description || this.formData.description,
            authentication: result.spec.authentication || 'OAuth 2.0',
            endpoints: result.spec.endpoints || [],
            securityRequirements: result.spec.securityRequirements || [
              'OAuth 2.0 authentication required',
              'Rate limiting: 100 requests per minute',
              'All requests must be sent over HTTPS'
            ],
            openapi_spec: result.spec.openapi_spec || ''
          }
          this.specGenerated = true
          
          // Scroll to result section
          this.$nextTick(() => {
            const resultSection = this.$el.querySelector('.spec-result-section')
            if (resultSection) {
              resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }
          })
        } else {
          alert('Failed to generate API specification: ' + (result.error || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error generating spec:', error)
        alert('Failed to generate API specification: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loading = false
      }
    },
    async copyOpenAPISpec() {
      if (!this.generatedSpec.openapi_spec) {
        alert('No OpenAPI specification available to copy')
        return
      }
      
      // Get the spec text - handle both string and escaped JSON string
      let specText = this.generatedSpec.openapi_spec
      
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
      
      // Try modern Clipboard API first (works in HTTPS and localhost)
      if (navigator.clipboard && navigator.clipboard.writeText) {
        try {
          await navigator.clipboard.writeText(specText)
          this.copySuccess = true
          setTimeout(() => {
            this.copySuccess = false
          }, 2000)
          return
        } catch (err) {
          console.error('Clipboard API failed:', err)
          // Fall through to fallback method
        }
      }
      
      // Fallback method for older browsers or when Clipboard API fails
      try {
        const textarea = document.createElement('textarea')
        textarea.value = specText
        textarea.style.position = 'fixed'
        textarea.style.left = '-9999px'
        textarea.style.top = '0'
        textarea.setAttribute('readonly', '')
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        
        // Select and copy
        if (navigator.userAgent.match(/ipad|iphone/i)) {
          // iOS workaround
          const range = document.createRange()
          range.selectNodeContents(textarea)
          const selection = window.getSelection()
          selection.removeAllRanges()
          selection.addRange(range)
          textarea.setSelectionRange(0, 999999)
        } else {
          textarea.select()
          textarea.setSelectionRange(0, specText.length)
        }
        
        const successful = document.execCommand('copy')
        document.body.removeChild(textarea)
        
        if (successful) {
          this.copySuccess = true
          setTimeout(() => {
            this.copySuccess = false
          }, 2000)
        } else {
          throw new Error('execCommand failed')
        }
      } catch (err) {
        console.error('Copy failed:', err)
        // Last resort: show the text in a prompt so user can copy manually
        const shouldShow = confirm('Failed to copy automatically. Would you like to see the OpenAPI spec in a dialog to copy manually?')
        if (shouldShow) {
          prompt('Copy this OpenAPI specification:', specText)
        }
      }
    },
    exportYAML() {
      if (!this.generatedSpec.openapi_spec) {
        alert('No OpenAPI specification available to export')
        return
      }
      
      // Get the spec text - handle both string and escaped JSON string
      let specText = this.generatedSpec.openapi_spec
      
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
      a.download = `${this.generatedSpec.serviceName.replace(/\s+/g, '_')}_API_Spec.yaml`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
    async exportPDF() {
      if (!this.generatedSpec.serviceName && !this.generatedSpec.openapi_spec) {
        alert('No API specification available to export')
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
        
        // Title
        addText(this.generatedSpec.serviceName || 'API Specification', 20, true, [151, 20, 77])
        yPos += 5
        
        // Service Information Section
        addText('Service Information', 14, true)
        yPos += 3
        
        doc.setFontSize(10)
        doc.setFont(undefined, 'normal')
        addText(`Version: ${this.generatedSpec.version || '1.0.0'}`, 10)
        addText(`Base URL: ${this.generatedSpec.baseUrl || 'Not specified'}`, 10)
        addText(`Description: ${this.generatedSpec.description || 'No description provided'}`, 10)
        addText(`Authentication: ${this.generatedSpec.authentication || 'OAuth 2.0'}`, 10)
        yPos += 5
        
        // Security Requirements Section
        if (this.generatedSpec.securityRequirements && this.generatedSpec.securityRequirements.length > 0) {
          addText('Security Requirements', 14, true)
          yPos += 3
          doc.setFontSize(10)
          this.generatedSpec.securityRequirements.forEach(req => {
            addText(`• ${req}`, 10)
          })
          yPos += 5
        }
        
        // Endpoints Section
        if (this.generatedSpec.endpoints && this.generatedSpec.endpoints.length > 0) {
          addText('API Endpoints', 14, true)
          yPos += 3
          
          this.generatedSpec.endpoints.forEach((endpoint, index) => {
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
        doc.save(`${this.generatedSpec.serviceName.replace(/\s+/g, '_')}_API_Documentation.pdf`)
      } catch (error) {
        console.error('PDF export error:', error)
        alert('Failed to export PDF. Error: ' + error.message)
      }
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
  background-color: rgba(255, 255, 255, 0.2);
}

.dialog-body {
  overflow-y: auto;
  flex: 1;
  padding: 0;
}

.dialog-body {
  padding: 2rem;
}

.how-it-works-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
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
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #f3e8ff;
  color: #97144D;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
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
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.step-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

.create-spec-section {
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 0 0 1rem 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.load-sample-button {
  background-color: #97144D;
  color: white;
  border: none;
}

.load-sample-button:hover {
  background-color: #7a0f3d;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #97144D;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.generate-button-container {
  margin-top: 1.5rem;
  margin-bottom: 0;
}

.generate-button {
  background-color: #97144D;
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  transition: all 0.2s;
}

.generate-button:hover:not(:disabled) {
  background-color: #7a0f3d;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(151, 20, 77, 0.2);
}

.generate-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.generate-button .spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.export-pdf-section {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  padding: 0 0.5rem;
}

.export-pdf-main-button {
  background-color: #97144D;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.export-pdf-main-button:hover {
  background-color: #7a103d;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(151, 20, 77, 0.2);
}

/* Spec Result Section */
.spec-result-section {
  margin: 0;
}

.spec-result-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}

.spec-result-content {
  padding: 2rem;
}

.spec-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.spec-title-section {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.export-pdf-header-button {
  background-color: #97144D;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.export-pdf-header-button:hover {
  background-color: #7a0f3d;
}

.success-icon {
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.spec-result-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.spec-result-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
}

.spec-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.spec-section {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e5e5;
}

.spec-section:last-of-type {
  border-bottom: none;
}

.spec-section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.spec-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.spec-info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.spec-info-item.full-width {
  grid-column: 1 / -1;
}

.spec-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
}

.spec-value {
  font-size: 0.875rem;
  color: #1f2937;
}

.spec-url-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: #f3f4f6;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #374151;
  font-family: monospace;
}

.endpoints-placeholder {
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 6px;
  text-align: center;
}

.placeholder-text {
  font-size: 0.875rem;
  color: #9ca3af;
  font-style: italic;
}

.endpoints-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.endpoint-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background-color: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e5e5;
}

.endpoint-method {
  padding: 0.25rem 0.75rem;
  background-color: #97144D;
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
}

.endpoint-path {
  font-family: monospace;
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
  flex: 1;
}

.endpoint-description {
  font-size: 0.875rem;
  color: #6b7280;
  flex: 2;
}

.security-requirements {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.security-requirements li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #374151;
}

.openapi-compliant-box {
  background-color: #f3e8ff;
  border: 1px solid #e9d5ff;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.openapi-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.openapi-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #97144D;
}

.openapi-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

.spec-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.spec-actions {
  display: flex;
  gap: 0.75rem;
}

.copy-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-yaml-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-color: #97144D;
  color: #97144D;
  background-color: white;
}

.export-yaml-button:hover {
  background-color: #97144D;
  color: white;
  border-color: #97144D;
}

.export-pdf-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #97144D;
  color: white;
}

.export-pdf-button:hover {
  background-color: #7a0f3d;
}

.openapi-spec-box {
  background-color: #1e1e1e;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.openapi-spec-content {
  color: #d4d4d4;
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.swagger-link {
  color: #97144D;
  text-decoration: underline;
  font-weight: 500;
}

.swagger-link:hover {
  color: #7a0f3d;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e5e5;
  margin-top: 2rem;
}

.pro-tip {
  font-size: 0.875rem;
  color: #6b7280;
}

.pro-tip strong {
  color: #374151;
}

@media (max-width: 768px) {
  .steps-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .dialog-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 640px) {
  .steps-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .spec-info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
