<template>
  <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-5xl max-h-[90vh] border-0 flex flex-col p-0">
      <!-- Header - Fixed -->
      <div class="dialog-header-gradient">
        <div class="dialog-header-content">
          <div class="flex items-center gap-3">
            <div class="header-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
              </svg>
            </div>
            <div>
              <DialogTitle class="header-title">Service Virtualization Agent</DialogTitle>
              <p class="header-subtitle">Create Mock APIs Instantly for Development & Testing</p>
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
        <Tabs v-model="activeMode" class="mode-tabs">
          <TabsList class="mode-tabs-list">
            <TabsTrigger value="ai" class="mode-tab">AI Mode</TabsTrigger>
            <TabsTrigger value="quick" class="mode-tab">Quick Mode</TabsTrigger>
          </TabsList>

          <!-- AI tab: free text only -->
          <TabsContent value="ai" class="mode-tab-content">
            <div class="create-mock-section">
              <div class="form-group">
                <Textarea 
                  v-model="formData.aiPrompt" 
                  placeholder="Describe the mock API you need... e.g. A users API with GET /users and GET /users/:id returning name and email"
                  rows="6"
                  class="form-textarea ai-textarea"
                />
              </div>
              <Button 
                variant="default" 
                class="generate-button" 
                @click="generateMockService"
                :disabled="loading"
              >
                <svg v-if="loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner">
                  <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                  <path d="M12 2 A10 10 0 0 1 22 12" stroke-linecap="round"></path>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
                </svg>
                {{ loading ? 'Generating...' : 'Generate Mock API' }}
              </Button>
            </div>
          </TabsContent>

          <!-- Quick Mode tab: Service Name, Method, Path, Status, Response Body, Latency + Advanced -->
          <TabsContent value="quick" class="mode-tab-content">
            <div class="create-mock-section">
              <div class="quick-fields">
                <div class="form-group">
                  <label class="form-label">Service Name</label>
                  <Input v-model="formData.serviceName" placeholder="e.g. My API" class="form-input" />
                </div>
                <div class="form-row">
                  <div class="form-group form-group-method">
                    <label class="form-label">Method</label>
                    <select v-model="formData.endpoints[0].method" class="form-select form-select-sm">
                      <option value="GET">GET</option>
                      <option value="POST">POST</option>
                      <option value="PUT">PUT</option>
                      <option value="PATCH">PATCH</option>
                      <option value="DELETE">DELETE</option>
                    </select>
                  </div>
                  <div class="form-group form-group-path">
                    <label class="form-label">Path</label>
                    <Input v-model="formData.endpoints[0].path" placeholder="e.g. /users" class="form-input" />
                  </div>
                  <div class="form-group form-group-status">
                    <label class="form-label">Status</label>
                    <select v-model="formData.endpoints[0].statusCode" class="form-select form-select-sm">
                      <option value="200">200</option>
                      <option value="201">201</option>
                      <option value="204">204</option>
                      <option value="400">400</option>
                      <option value="401">401</option>
                      <option value="404">404</option>
                      <option value="500">500</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Response Body</label>
                  <Textarea 
                    v-model="formData.endpoints[0].responseBody" 
                    placeholder='{ "id": 1, "name": "Sample" }'
                    rows="4"
                    class="form-textarea mono"
                  />
                </div>
                <div class="form-group latency-row">
                  <label class="latency-checkbox-label">
                    <input type="checkbox" v-model="formData.endpoints[0].addDelay" class="latency-checkbox" />
                    <span>Add latency</span>
                  </label>
                  <Input 
                    v-if="formData.endpoints[0].addDelay"
                    v-model="formData.endpoints[0].delay" 
                    type="number" 
                    placeholder="ms"
                    class="form-input form-input-latency"
                  />
                </div>
              </div>

              <div class="generate-button-container">
                <Button 
                  variant="default" 
                  class="generate-button" 
                  @click="generateMockService"
                  :disabled="loading"
                >
                  <svg v-if="loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner">
                    <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                    <path d="M12 2 A10 10 0 0 1 22 12" stroke-linecap="round"></path>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                  {{ loading ? 'Generating...' : 'Generate Mock API' }}
                </Button>
              </div>
            </div>
          </TabsContent>
        </Tabs>

        <!-- Generated Mock Service Result -->
        <div v-if="mockGenerated" class="mock-result-section">
          <Card class="mock-result-card">
            <CardContent class="mock-result-content">
              <div class="mock-result-header">
                <div class="mock-result-title-section">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" class="success-icon">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <div>
                    <h3 class="mock-result-title">Mock Service Generated Successfully</h3>
                    <p class="mock-result-subtitle">Your mock API is ready to use</p>
                  </div>
                </div>
              </div>

              <!-- Mock Server URL -->
              <div class="server-url-section">
                <div class="server-url-label">Mock Server URL</div>
                <div class="server-url-box">
                  <code class="server-url-text">{{ generatedMock.serverUrl }}</code>
                  <Button variant="outline" size="sm" @click="copyServerUrl" class="copy-url-button">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    {{ copyUrlSuccess ? 'Copied!' : 'Copy' }}
                  </Button>
                </div>
              </div>

              <!-- Generated Endpoints Summary -->
              <div class="generated-endpoints-section">
                <h4 class="generated-endpoints-title">Available Endpoints</h4>
                <div class="generated-endpoints-list">
                  <div v-for="(ep, index) in generatedMock.endpoints" :key="index" class="generated-endpoint-item">
                    <div :class="['method-badge', ep.method.toLowerCase()]">{{ ep.method }}</div>
                    <div class="endpoint-info">
                      <code class="endpoint-path-text">{{ generatedMock.serverUrl }}{{ ep.path }}</code>
                      <span class="endpoint-desc-text">{{ ep.description }}</span>
                    </div>
                    <div class="endpoint-status-badge">{{ ep.statusCode }}</div>
                  </div>
                </div>
              </div>

              <!-- Sample cURL -->
              <div class="curl-section">
                <div class="curl-header">
                  <h4 class="curl-title">Quick Test (cURL)</h4>
                  <Button variant="outline" size="sm" @click="copyCurl" class="copy-curl-button">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    {{ copyCurlSuccess ? 'Copied!' : 'Copy' }}
                  </Button>
                </div>
                <div class="curl-box">
                  <pre class="curl-content">{{ generatedCurl }}</pre>
                </div>
              </div>

              <!-- Actions -->
              <div class="result-actions">
                <Button variant="outline" class="action-button" @click="exportPostmanCollection">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Export Postman Collection
                </Button>
                <Button variant="outline" class="action-button" @click="exportOpenAPISpec">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                  </svg>
                  Export OpenAPI Spec
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script>
import { Dialog, DialogContent, DialogTitle, DialogClose } from './ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Card, CardContent } from './ui/card'

export default {
  name: 'ServiceVirtualizationAgentDialog',
  components: {
    Dialog,
    DialogContent,
    DialogTitle,
    DialogClose,
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
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
      loading: false,
      mockGenerated: false,
      copyUrlSuccess: false,
      copyCurlSuccess: false,
      activeMode: 'ai',
      formData: {
        aiPrompt: '',
        serviceName: '',
        endpoints: [
          {
            method: 'GET',
            path: '/data',
            statusCode: '200',
            responseBody: '',
            addDelay: false,
            delay: '200'
          }
        ]
      },
      generatedMock: {
        serverUrl: '',
        endpoints: []
      },
      defaultResponseBody: JSON.stringify(
        { data: [{ id: 1, name: 'Sample Item', status: 'active' }], total: 1 },
        null,
        2
      )
    }
  },
  computed: {
    generatedCurl() {
      if (!this.generatedMock.endpoints || this.generatedMock.endpoints.length === 0) return ''
      const firstGet = this.generatedMock.endpoints.find(e => e.method === 'GET') || this.generatedMock.endpoints[0]
      return `curl -X ${firstGet.method} "${this.generatedMock.serverUrl}${firstGet.path}" \\\n  -H "Content-Type: application/json"`
    },
    effectiveServiceName() {
      if (this.activeMode === 'quick' && (this.formData.serviceName || '').trim()) {
        return this.formData.serviceName.trim()
      }
      return (this.deriveDefaultsFromAiPrompt().serviceName || 'Mock Service').trim()
    }
  },
  methods: {
    deriveDefaultsFromAiPrompt() {
      const what = (this.formData.aiPrompt || '').trim()
      if (!what) {
        return {
          serviceName: 'My Mock API',
          baseUrl: '/api/v1',
          path: '/data'
        }
      }
      const words = what.split(/\s+/).filter(Boolean)
      const first = words[0].toLowerCase().replace(/[^a-z0-9]/g, '')
      const name = what.charAt(0).toUpperCase() + what.slice(1).replace(/\b\w/g, c => c.toUpperCase())
      const path = first ? `/${first}` : '/data'
      return {
        serviceName: name,
        baseUrl: '/api/v1',
        path
      }
    },
    getEndpointsForGeneration() {
      if (this.activeMode === 'quick') {
        const ep = this.formData.endpoints[0]
        return [{
          method: ep.method,
          path: (ep.path || '').trim() || '/data',
          statusCode: ep.statusCode,
          description: `${ep.method} ${(ep.path || '').trim() || '/data'}`,
          responseBody: (ep.responseBody || '').trim() || this.defaultResponseBody,
          delay: ep.addDelay ? (parseInt(ep.delay) || 0) : 0
        }]
      }
      const defaults = this.deriveDefaultsFromAiPrompt()
      return [
        {
          method: 'GET',
          path: defaults.path,
          statusCode: '200',
          description: `${defaults.path} endpoint`,
          responseBody: this.defaultResponseBody,
          delay: 0
        }
      ]
    },
    async generateMockService() {
      this.loading = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1200))

        const endpoints = this.getEndpointsForGeneration()
        const baseUrl = '/api/v1'

        this.generatedMock = {
          serverUrl: `https://mock.axisbank.dev${baseUrl}`,
          endpoints: endpoints.map(ep => ({
            method: ep.method,
            path: ep.path,
            statusCode: ep.statusCode,
            description: ep.description || `${ep.method} ${ep.path}`,
            responseBody: ep.responseBody,
            delay: ep.delay
          }))
        }
        this.mockGenerated = true

        this.$nextTick(() => {
          const resultSection = this.$el.querySelector('.mock-result-section')
          if (resultSection) {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        })
      } catch (error) {
        console.error('Error generating mock service:', error)
        alert('Failed to generate mock service: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async copyServerUrl() {
      try {
        await navigator.clipboard.writeText(this.generatedMock.serverUrl)
        this.copyUrlSuccess = true
        setTimeout(() => { this.copyUrlSuccess = false }, 2000)
      } catch {
        this.fallbackCopy(this.generatedMock.serverUrl)
      }
    },
    async copyCurl() {
      try {
        await navigator.clipboard.writeText(this.generatedCurl)
        this.copyCurlSuccess = true
        setTimeout(() => { this.copyCurlSuccess = false }, 2000)
      } catch {
        this.fallbackCopy(this.generatedCurl)
      }
    },
    fallbackCopy(text) {
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.style.position = 'fixed'
      textarea.style.left = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    },
    exportPostmanCollection() {
      const collection = {
        info: {
          name: this.effectiveServiceName,
          schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
        },
        item: this.generatedMock.endpoints.map(ep => ({
          name: ep.description || `${ep.method} ${ep.path}`,
          request: {
            method: ep.method,
            url: `${this.generatedMock.serverUrl}${ep.path}`,
            header: [{ key: 'Content-Type', value: 'application/json' }]
          }
        }))
      }
      const blob = new Blob([JSON.stringify(collection, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${this.effectiveServiceName.replace(/\s+/g, '_')}_postman.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
    exportOpenAPISpec() {
      const paths = {}
      this.generatedMock.endpoints.forEach(ep => {
        const pathKey = ep.path.replace(/:(\w+)/g, '{$1}')
        if (!paths[pathKey]) paths[pathKey] = {}
        paths[pathKey][ep.method.toLowerCase()] = {
          summary: ep.description,
          responses: {
            [ep.statusCode]: {
              description: ep.description,
              content: ep.responseBody ? { 'application/json': { example: (() => { try { return JSON.parse(ep.responseBody) } catch { return {} } })() } } : undefined
            }
          }
        }
      })
      const spec = `openapi: "3.0.0"\ninfo:\n  title: "${this.effectiveServiceName}"\n  version: "1.0.0"\nservers:\n  - url: "${this.generatedMock.serverUrl}"\npaths:\n${Object.entries(paths).map(([path, methods]) => 
        `  ${path}:\n${Object.entries(methods).map(([method, details]) => 
          `    ${method}:\n      summary: "${details.summary}"\n      responses:\n        "${Object.keys(details.responses)[0]}":\n          description: "${details.summary}"`
        ).join('\n')}`
      ).join('\n')}`

      const blob = new Blob([spec], { type: 'text/yaml;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${this.effectiveServiceName.replace(/\s+/g, '_')}_openapi.yaml`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
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
  padding: 2rem;
  background: #f5f5f5;
}

/* Mode tabs: AI | Quick Mode */
.mode-tabs {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.mode-tabs-list {
  display: flex;
  gap: 0.25rem;
  background: #e5e7eb;
  padding: 0.25rem;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1.5rem;
}

.mode-tab {
  padding: 0.5rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 6px;
}

.mode-tab[data-state="active"] {
  background: white;
  color: #97144D;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.mode-tab-content {
  margin-top: 0;
}

.ai-textarea {
  min-height: 140px;
  font-size: 0.9375rem;
}

.quick-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 90px 1fr 90px;
  gap: 1rem;
}

.form-group-method .form-select,
.form-group-status .form-select {
  width: 100%;
  min-width: 0;
}

.form-select-sm {
  width: 100%;
  max-width: 90px;
}

.form-group-path {
  min-width: 0;
}

/* Override form-group column layout so checkbox + input stay on one row */
.form-group.latency-row {
  flex-direction: row;
  align-items: center;
  gap: 0.75rem;
  justify-content: flex-start;
}

.latency-checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  flex-shrink: 0;
}

.latency-checkbox {
  accent-color: #97144D;
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.form-input-latency {
  width: 70px !important;
  min-width: 70px !important;
  max-width: 70px !important;
  flex: 0 0 70px;
  padding: 0.5rem 0.375rem;
  font-size: 0.875rem;
  box-sizing: border-box;
}

/* How It Works */
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
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
}

.step-icon.blue { background-color: #dbeafe; color: #3b82f6; }
.step-icon.purple { background-color: #f3e8ff; color: #97144D; }
.step-icon.pink { background-color: #fce7f3; color: #ec4899; }
.step-icon.green { background-color: #d1fae5; color: #10b981; }

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

/* Create Mock Section */
.create-mock-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e5e5e5;
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header .section-title {
  margin-bottom: 0;
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
  margin-bottom: 0.75rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.375rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
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
}

.form-textarea.mono {
  font-family: 'Courier New', monospace;
  font-size: 0.8125rem;
}

.form-select {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #97144D;
}

/* Endpoints */
.endpoints-section {
  margin-top: 1.5rem;
}

.endpoints-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.endpoints-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.add-endpoint-button {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  border-color: #97144D;
  color: #97144D;
}

.add-endpoint-button:hover {
  background-color: #97144D;
  color: white;
}

.endpoints-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.endpoint-form-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.25rem;
}

.endpoint-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.endpoint-form-number {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #97144D;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.remove-endpoint-button {
  background: none;
  border: none;
  padding: 0.375rem;
  cursor: pointer;
  color: #9ca3af;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-endpoint-button:hover {
  color: #ef4444;
  background: #fee2e2;
}

.endpoint-form-grid {
  display: grid;
  grid-template-columns: 120px 1fr 150px;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.endpoint-options {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.option-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #6b7280;
  cursor: pointer;
}

.option-checkbox {
  accent-color: #97144D;
}

.delay-input {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.delay-field {
  width: 80px;
}

.delay-unit {
  font-size: 0.8125rem;
  color: #6b7280;
}

/* Generate Button */
.generate-button-container {
  margin-top: 1.5rem;
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
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Result Section */
.mock-result-section {
  margin-top: 1.5rem;
}

.mock-result-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
}

.mock-result-content {
  padding: 2rem;
}

.mock-result-header {
  margin-bottom: 1.5rem;
}

.mock-result-title-section {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.success-icon {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.mock-result-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.mock-result-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

/* Server URL */
.server-url-section {
  margin-bottom: 1.5rem;
}

.server-url-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.server-url-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  padding: 0.875rem 1rem;
}

.server-url-text {
  flex: 1;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #166534;
  font-family: 'Courier New', monospace;
}

.copy-url-button {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  flex-shrink: 0;
}

/* Generated Endpoints */
.generated-endpoints-section {
  margin-bottom: 1.5rem;
}

.generated-endpoints-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.generated-endpoints-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.generated-endpoint-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.method-badge {
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.6875rem;
  font-weight: 700;
  min-width: 56px;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.method-badge.get { background: #dbeafe; color: #1e40af; }
.method-badge.post { background: #d1fae5; color: #065f46; }
.method-badge.put { background: #fef3c7; color: #92400e; }
.method-badge.patch { background: #fce7f3; color: #9d174d; }
.method-badge.delete { background: #fee2e2; color: #991b1b; }

.endpoint-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.endpoint-path-text {
  font-size: 0.8125rem;
  color: #1f2937;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.endpoint-desc-text {
  font-size: 0.75rem;
  color: #6b7280;
}

.endpoint-status-badge {
  padding: 0.25rem 0.5rem;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  flex-shrink: 0;
}

/* cURL Section */
.curl-section {
  margin-bottom: 1.5rem;
}

.curl-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.curl-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.copy-curl-button {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.curl-box {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 1rem;
}

.curl-content {
  color: #d4d4d4;
  font-family: 'Courier New', monospace;
  font-size: 0.8125rem;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Result Actions */
.result-actions {
  display: flex;
  gap: 0.75rem;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-color: #97144D;
  color: #97144D;
}

.action-button:hover {
  background-color: #97144D;
  color: white;
  border-color: #97144D;
}

/* Responsive */
@media (max-width: 768px) {
  .steps-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .endpoint-form-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .result-actions {
    flex-direction: column;
  }

  .generated-endpoint-item {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .steps-grid {
    grid-template-columns: 1fr;
  }

  .dialog-body {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
