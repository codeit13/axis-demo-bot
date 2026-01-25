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

      <!-- Output Content -->
      <Card class="output-card">
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

export default {
  name: 'AgentRunOutput',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Badge
  },
  data() {
    return {
      loading: true,
      error: null,
      suggestion: null,
      processing: false
    }
  },
  computed: {
    parsedContent() {
      if (!this.suggestion || !this.suggestion.content) return null
      try {
        return JSON.parse(this.suggestion.content)
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
}
</style>
