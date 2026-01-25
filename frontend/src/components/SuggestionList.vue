<template>
  <div class="suggestion-list">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold">AI Suggestions</h2>
      <div class="flex gap-2">
        <Select v-model="filters.agent_type" @update:modelValue="filters.agent_type = $event || ''; updateFilters()" class="w-auto">
          <SelectTrigger class="w-auto">
            <SelectValue placeholder="All Agents" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="unit_test">Unit Test</SelectItem>
            <SelectItem value="api_spec">API Spec</SelectItem>
            <SelectItem value="business_logic">Business Logic</SelectItem>
            <SelectItem value="bug_scanner">Bug Scanner</SelectItem>
            <SelectItem value="code_review">Code Review</SelectItem>
            <SelectItem value="documentation">Documentation</SelectItem>
          </SelectContent>
        </Select>
        <Select v-model="filters.status" @update:modelValue="filters.status = $event || ''; updateFilters()" class="w-auto">
          <SelectTrigger class="w-auto">
            <SelectValue placeholder="All Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
            <SelectItem value="rejected">Rejected</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <div v-if="suggestions.length === 0" class="text-center py-12 text-gray-500">
      <p>No suggestions found. Run an agent from the Dashboard to generate suggestions.</p>
    </div>

    <Card v-for="suggestion in suggestions" :key="suggestion.id" class="mb-6">
      <CardHeader>
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-3">
            <CardTitle class="text-lg">{{ formatAgentType(suggestion.agent_type) }}</CardTitle>
            <Badge :variant="suggestion.status">{{ suggestion.status }}</Badge>
          </div>
          <div class="text-sm text-gray-500">
            {{ formatDate(suggestion.created_at) }}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <!-- Metadata -->
        <div class="flex gap-4 mb-4 text-sm">
          <div v-if="suggestion.code_file_id" class="flex items-center gap-2">
            <span class="text-gray-500">File ID:</span>
            <span class="font-medium">{{ suggestion.code_file_id }}</span>
          </div>
          <div v-if="suggestion.issue_id" class="flex items-center gap-2">
            <span class="text-gray-500">Issue ID:</span>
            <span class="font-medium">{{ suggestion.issue_id }}</span>
          </div>
        </div>

        <!-- Parsed Content Preview -->
        <div class="suggestion-preview">
          <div v-if="parsedContent(suggestion).summary" class="mb-4">
            <h4 class="font-semibold text-sm mb-2 text-gray-700">Summary</h4>
            <p class="text-sm text-gray-600 bg-blue-50 p-3 rounded">{{ parsedContent(suggestion).summary }}</p>
          </div>

          <!-- Unit Test Agent -->
          <div v-if="suggestion.agent_type === 'unit_test'" class="mb-4">
            <div v-if="parsedContent(suggestion).explanation && parsedContent(suggestion).explanation !== 'Generated unit tests'" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Explanation</h4>
              <p class="text-sm text-gray-700 bg-blue-50 p-3 rounded">{{ parsedContent(suggestion).explanation }}</p>
            </div>
            
            <div v-if="parsedContent(suggestion).test_code" class="mb-4">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-semibold text-sm text-gray-700">Test Code</h4>
                <button 
                  @click="copyToClipboard(extractCode(parsedContent(suggestion).test_code), $event)"
                  class="text-xs text-purple-600 hover:text-purple-700 px-2 py-1 rounded hover:bg-purple-50 transition-colors"
                >
                  📋 Copy Code
                </button>
              </div>
              <div class="code-block">
                <pre><code>{{ extractCode(parsedContent(suggestion).test_code) }}</code></pre>
              </div>
            </div>
            
            <div v-if="parsedContent(suggestion).test_cases && parsedContent(suggestion).test_cases.length > 0" class="mt-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Test Cases Covered</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <div 
                  v-for="(testCase, idx) in parsedContent(suggestion).test_cases" 
                  :key="idx"
                  class="bg-gray-50 p-2 rounded text-sm text-gray-700 border-l-2 border-purple-400"
                >
                  <span class="text-purple-600 font-medium">#{{ idx + 1 }}</span> {{ testCase }}
                </div>
              </div>
            </div>
          </div>

          <!-- API Spec Agent -->
          <div v-if="suggestion.agent_type === 'api_spec' && parsedContent(suggestion).openapi_spec" class="mb-4">
            <h4 class="font-semibold text-sm mb-2 text-gray-700">OpenAPI Specification</h4>
            <div class="code-block">
              <pre><code>{{ parsedContent(suggestion).openapi_spec }}</code></pre>
            </div>
          </div>

          <!-- Bug Scanner Agent -->
          <div v-if="suggestion.agent_type === 'bug_scanner'">
            <div v-if="parsedContent(suggestion).bug_explanation" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Bug Explanation</h4>
              <p class="text-sm text-gray-700 bg-red-50 p-3 rounded">{{ parsedContent(suggestion).bug_explanation }}</p>
            </div>
            <div v-if="parsedContent(suggestion).suggested_fix" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Suggested Fix</h4>
              <div class="code-block">
                <pre><code>{{ extractCode(parsedContent(suggestion).suggested_fix) }}</code></pre>
              </div>
            </div>
            <div v-if="parsedContent(suggestion).root_cause" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Root Cause</h4>
              <p class="text-sm text-gray-700 bg-yellow-50 p-3 rounded">{{ parsedContent(suggestion).root_cause }}</p>
            </div>
          </div>

          <!-- Code Review Agent -->
          <div v-if="suggestion.agent_type === 'code_review'">
            <div v-if="parsedContent(suggestion).overall_rating" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Overall Rating</h4>
              <Badge :variant="getRatingVariant(parsedContent(suggestion).overall_rating)">
                {{ parsedContent(suggestion).overall_rating }}
              </Badge>
            </div>
            <div v-if="parsedContent(suggestion).issues && parsedContent(suggestion).issues.length > 0" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Issues Found</h4>
              <div v-for="(issue, idx) in parsedContent(suggestion).issues" :key="idx" class="mb-3 p-3 bg-yellow-50 rounded border-l-4 border-yellow-400">
                <div class="flex items-center gap-2 mb-1">
                  <Badge :variant="issue.severity === 'high' ? 'destructive' : 'secondary'">{{ issue.severity }}</Badge>
                  <span class="text-xs text-gray-500">{{ issue.type }}</span>
                </div>
                <p class="text-sm text-gray-700 mb-2">{{ issue.description }}</p>
                <p v-if="issue.suggestion" class="text-sm text-gray-600"><strong>Suggestion:</strong> {{ issue.suggestion }}</p>
                <div v-if="issue.code_example" class="mt-2 code-block">
                  <pre><code>{{ extractCode(issue.code_example) }}</code></pre>
                </div>
              </div>
            </div>
          </div>

          <!-- Business Logic Agent -->
          <div v-if="suggestion.agent_type === 'business_logic'">
            <div v-if="parsedContent(suggestion).analysis" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Analysis</h4>
              <p class="text-sm text-gray-700 bg-gray-50 p-3 rounded whitespace-pre-wrap">{{ parsedContent(suggestion).analysis }}</p>
            </div>
            <div v-if="parsedContent(suggestion).suggestions && parsedContent(suggestion).suggestions.length > 0" class="mb-4">
              <h4 class="font-semibold text-sm mb-2 text-gray-700">Suggestions</h4>
              <ul class="list-disc list-inside text-sm text-gray-700 space-y-1 bg-gray-50 p-3 rounded">
                <li v-for="(suggestion, idx) in parsedContent(suggestion).suggestions" :key="idx">{{ suggestion }}</li>
              </ul>
            </div>
          </div>

          <!-- Documentation Agent -->
          <div v-if="suggestion.agent_type === 'documentation' && parsedContent(suggestion).documentation" class="mb-4">
            <h4 class="font-semibold text-sm mb-2 text-gray-700">Documentation</h4>
            <div class="code-block">
              <pre><code>{{ parsedContent(suggestion).documentation }}</code></pre>
            </div>
          </div>

          <!-- Fallback for unparsed content -->
          <div v-if="!hasStructuredContent(suggestion)" class="code-block">
            <pre><code>{{ formatContent(suggestion.content) }}</code></pre>
          </div>
        </div>

        <!-- Action Buttons -->
        <div v-if="suggestion.status === 'pending'" class="flex gap-2 mt-6 pt-4 border-t">
          <Button @click="approveSuggestion(suggestion.id)" variant="default" class="bg-green-600 hover:bg-green-700">
            ✓ Approve
          </Button>
          <Button @click="rejectSuggestion(suggestion.id)" variant="destructive">
            ✗ Reject
          </Button>
          <Button @click="viewDetails(suggestion.id)" variant="secondary">
            View Full Details
          </Button>
        </div>

        <div v-else class="mt-6 pt-4 border-t text-gray-600">
          <div class="flex items-center justify-between">
            <span><strong>Status:</strong> {{ suggestion.status }}</span>
            <Button @click="viewDetails(suggestion.id)" variant="secondary">
              View Full Details
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Enhanced Detail Dialog -->
    <Dialog :open="!!selectedSuggestion" @update:open="selectedSuggestion = null">
      <DialogTitle class="text-xl">
        {{ selectedSuggestion ? formatAgentType(selectedSuggestion.agent_type) + ' - Full Details' : '' }}
      </DialogTitle>
      <DialogContent>
        <div v-if="selectedSuggestion" class="space-y-4">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-500">Status:</span>
              <Badge :variant="selectedSuggestion.status" class="ml-2">{{ selectedSuggestion.status }}</Badge>
            </div>
            <div>
              <span class="text-gray-500">Created:</span>
              <span class="ml-2">{{ formatDate(selectedSuggestion.created_at) }}</span>
            </div>
            <div v-if="selectedSuggestion.code_file_id">
              <span class="text-gray-500">File ID:</span>
              <span class="ml-2 font-medium">{{ selectedSuggestion.code_file_id }}</span>
            </div>
            <div v-if="selectedSuggestion.issue_id">
              <span class="text-gray-500">Issue ID:</span>
              <span class="ml-2 font-medium">{{ selectedSuggestion.issue_id }}</span>
            </div>
          </div>

          <div class="border-t pt-4">
            <h4 class="font-semibold mb-3">Complete Content</h4>
            <div class="code-block-large">
              <pre><code>{{ formatContent(selectedSuggestion.content) }}</code></pre>
            </div>
          </div>
        </div>
      </DialogContent>
      <DialogFooter>
        <Button @click="selectedSuggestion = null" variant="secondary">Close</Button>
        <Button 
          v-if="selectedSuggestion && selectedSuggestion.status === 'pending'"
          @click="approveSuggestion(selectedSuggestion.id)" 
          variant="default" 
          class="bg-green-600 hover:bg-green-700"
        >
          Approve
        </Button>
      </DialogFooter>
    </Dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Badge } from './ui/badge'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from './ui/dialog'

export default {
  name: 'SuggestionList',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Select,
    SelectTrigger,
    SelectValue,
    SelectContent,
    SelectItem,
    Badge,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogFooter
  },
  data() {
    return {
      filters: {
        agent_type: '',
        status: ''
      },
      selectedSuggestion: null
    }
  },
  computed: {
    ...mapState('suggestions', ['suggestions', 'loading'])
  },
  async mounted() {
    await this.fetchSuggestions()
  },
  watch: {
    filters: {
      deep: true,
      handler() {
        this.updateFilters()
      }
    }
  },
  methods: {
    ...mapActions('suggestions', ['fetchSuggestions', 'approveSuggestion', 'fetchSuggestion', 'setFilters']),
    async updateFilters() {
      this.setFilters(this.filters)
    },
    async approveSuggestion(id) {
      try {
        await this.$store.dispatch('suggestions/approveSuggestion', {
          suggestionId: id,
          action: 'approve',
          comments: 'Approved by user'
        })
        if (this.selectedSuggestion && this.selectedSuggestion.id === id) {
          this.selectedSuggestion = null
        }
      } catch (error) {
        alert('Failed to approve suggestion: ' + (error.response?.data?.detail || error.message))
      }
    },
    async rejectSuggestion(id) {
      const reason = prompt('Reason for rejection (optional):')
      try {
        await this.$store.dispatch('suggestions/approveSuggestion', {
          suggestionId: id,
          action: 'reject',
          comments: reason || 'Rejected by user'
        })
        if (this.selectedSuggestion && this.selectedSuggestion.id === id) {
          this.selectedSuggestion = null
        }
      } catch (error) {
        alert('Failed to reject suggestion: ' + (error.response?.data?.detail || error.message))
      }
    },
    async viewDetails(id) {
      try {
        await this.fetchSuggestion(id)
        this.selectedSuggestion = this.$store.state.suggestions.currentSuggestion
      } catch (error) {
        console.error('Failed to load suggestion details:', error)
      }
    },
    formatAgentType(type) {
      return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    },
    formatContent(content) {
      try {
        const parsed = JSON.parse(content)
        return JSON.stringify(parsed, null, 2)
      } catch {
        return content
      }
    },
    parsedContent(suggestion) {
      try {
        const outer = JSON.parse(suggestion.content)
        
        // Handle nested JSON in test_code field (common in unit_test agent)
        if (outer.test_code && typeof outer.test_code === 'string') {
          // Remove markdown code blocks
          let innerJsonStr = outer.test_code
            .replace(/```json\n?/g, '')
            .replace(/```\n?/g, '')
            .trim()
          
          // Try to parse the inner JSON
          try {
            const inner = JSON.parse(innerJsonStr)
            // Merge inner content with outer, prioritizing inner
            return {
              ...outer,
              test_code: inner.test_code || outer.test_code,
              test_cases: inner.test_cases || outer.test_cases,
              explanation: inner.explanation || outer.explanation
            }
          } catch {
            // If inner JSON parse fails, try to extract just the code
            const codeMatch = innerJsonStr.match(/"test_code"\s*:\s*"([^"]+)"/)
            if (codeMatch) {
              // Unescape the string
              const unescaped = codeMatch[1]
                .replace(/\\n/g, '\n')
                .replace(/\\"/g, '"')
                .replace(/\\\\/g, '\\')
              return {
                ...outer,
                test_code: unescaped
              }
            }
          }
        }
        
        return outer
      } catch {
        return { content: suggestion.content }
      }
    },
    hasStructuredContent(suggestion) {
      const parsed = this.parsedContent(suggestion)
      return parsed && typeof parsed === 'object' && Object.keys(parsed).length > 1
    },
    extractCode(codeString) {
      if (!codeString) return ''
      
      // If it's already clean code, return it
      if (!codeString.includes('```') && !codeString.includes('\\n')) {
        return codeString.trim()
      }
      
      // Remove markdown code blocks
      let code = codeString
        .replace(/```json\n?/g, '')
        .replace(/```python\n?/g, '')
        .replace(/```\n?/g, '')
        .trim()
      
      // Unescape common escape sequences
      code = code
        .replace(/\\n/g, '\n')
        .replace(/\\"/g, '"')
        .replace(/\\t/g, '\t')
        .replace(/\\\\/g, '\\')
      
      // If it looks like JSON, try to parse and extract
      if (code.startsWith('{') || code.includes('"test_code"')) {
        try {
          const parsed = JSON.parse(code)
          if (parsed.test_code) {
            // Unescape the test_code string
            return parsed.test_code
              .replace(/\\n/g, '\n')
              .replace(/\\"/g, '"')
              .replace(/\\t/g, '\t')
              .replace(/\\\\/g, '\\')
          }
          if (parsed.suggested_fix) {
            return parsed.suggested_fix
              .replace(/\\n/g, '\n')
              .replace(/\\"/g, '"')
              .replace(/\\t/g, '\t')
              .replace(/\\\\/g, '\\')
          }
        } catch {
          // If JSON parse fails, try regex extraction
          const codeMatch = code.match(/"test_code"\s*:\s*"((?:[^"\\]|\\.)*)"/)
          if (codeMatch) {
            return codeMatch[1]
              .replace(/\\n/g, '\n')
              .replace(/\\"/g, '"')
              .replace(/\\t/g, '\t')
              .replace(/\\\\/g, '\\')
          }
        }
      }
      
      return code.trim()
    },
    getRatingVariant(rating) {
      if (!rating) return 'default'
      const lower = rating.toLowerCase()
      if (lower.includes('excellent') || lower.includes('good')) return 'approved'
      if (lower.includes('needs')) return 'pending'
      return 'default'
    },
    async copyToClipboard(text, event) {
      try {
        await navigator.clipboard.writeText(text)
        // Show a brief success message
        if (event && event.target) {
          const button = event.target
          const originalText = button.textContent
          button.textContent = '✓ Copied!'
          setTimeout(() => {
            button.textContent = originalText
          }, 2000)
        }
      } catch (err) {
        console.error('Failed to copy:', err)
        alert('Failed to copy to clipboard')
      }
    }
  }
}
</script>

<style scoped>
.suggestion-list {
  padding: 2rem 0;
}

.code-block {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}

.code-block pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.code-block code {
  color: #d4d4d4;
}

.code-block-large {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1.5rem;
  border-radius: 6px;
  overflow-x: auto;
  max-height: 60vh;
  overflow-y: auto;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}

.code-block-large pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.code-block-large code {
  color: #d4d4d4;
}

.suggestion-preview {
  max-height: 500px;
  overflow-y: auto;
}
</style>
