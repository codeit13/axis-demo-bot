<template>
  <div class="project-detail">
    <!-- Header -->
    <div class="mb-8">
      <Button @click="$router.push('/')" variant="ghost" size="sm" class="mb-4">
        ← Back to Projects
      </Button>
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-3xl font-bold mb-2">{{ project?.name || 'Loading...' }}</h1>
          <p class="text-gray-600">{{ project?.description || 'No description' }}</p>
        </div>
        <div class="flex gap-2">
          <Button @click="showRunAgents = true" variant="default">
            Run Agents
          </Button>
        </div>
      </div>
    </div>

    <!-- Agent Sections -->
    <div class="space-y-6">
      <!-- Business Logic & Policy -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">1️⃣</span>
                <span>Business Logic & Policy</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Canonical source for business rules with Rule IDs</p>
            </div>
            <Button 
              @click="handleBusinessLogicRun" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'business_logic_policy'"
            >
              {{ runningAgent === 'business_logic_policy' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="businessRules.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No business rules yet. Describe your business logic and run the Business Logic Agent to get started.</p>
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="rule in businessRules" 
              :key="rule.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-start mb-2">
                <div class="flex items-center gap-2">
                  <Badge :variant="getStatusVariant(rule.status)">{{ rule.rule_id }}</Badge>
                  <span class="text-sm text-gray-500">v{{ rule.version }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <Badge :variant="rule.status === 'approved' ? 'default' : 'secondary'">
                    {{ rule.status }}
                  </Badge>
                  <div v-if="rule.status !== 'approved'" class="flex gap-1">
                    <Button 
                      @click="approveRule(rule.rule_id)" 
                      variant="default"
                      size="sm"
                      :disabled="approvingRule === rule.rule_id"
                    >
                      {{ approvingRule === rule.rule_id ? 'Approving...' : 'Approve' }}
                    </Button>
                    <Button 
                      @click="rejectRule(rule.rule_id)" 
                      variant="outline"
                      size="sm"
                      :disabled="approvingRule === rule.rule_id"
                    >
                      Reject
                    </Button>
                  </div>
                </div>
              </div>
              <p class="text-sm whitespace-pre-wrap mb-2">{{ rule.content }}</p>
              <div v-if="rule.assumptions" class="text-xs text-gray-600 mt-2">
                <strong>Assumptions:</strong> {{ formatAssumptions(rule.assumptions) }}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Product & Requirements -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">2️⃣</span>
                <span>Product & Requirements</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Product requirements and NFRs derived from business logic</p>
            </div>
            <Button 
              @click="runAgent('product_requirements')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'product_requirements' || businessRules.length === 0"
            >
              {{ runningAgent === 'product_requirements' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="productRequirements.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No product requirements yet. Run the Product & Requirements Agent.</p>
            <p class="text-xs mt-1" v-if="businessRules.length === 0">Requires approved business rules first.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="suggestion in productRequirements" 
              :key="suggestion.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge variant="outline">Suggestion #{{ suggestion.id }}</Badge>
                <Badge :variant="suggestion.status === 'approved' ? 'default' : 'secondary'">
                  {{ suggestion.status }}
                </Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(suggestion.content)"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- API & Contracts -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">3️⃣</span>
                <span>API & Contracts</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">OpenAPI specifications and API contracts</p>
            </div>
            <Button 
              @click="runAgent('api_contract')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'api_contract' || businessRules.length === 0"
            >
              {{ runningAgent === 'api_contract' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="apiContracts.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No API contracts yet. Run the API & Contract Agent.</p>
            <p class="text-xs mt-1" v-if="businessRules.length === 0">Requires approved business rules first.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="suggestion in apiContracts" 
              :key="suggestion.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge variant="outline">API Spec #{{ suggestion.id }}</Badge>
                <Badge :variant="suggestion.status === 'approved' ? 'default' : 'secondary'">
                  {{ suggestion.status }}
                </Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(suggestion.content)"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Technical Architecture -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">4️⃣</span>
                <span>Technical Architecture</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Tech stack, patterns, and architectural decisions</p>
            </div>
            <Button 
              @click="runAgent('technical_architecture')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'technical_architecture' || businessRules.length === 0"
            >
              {{ runningAgent === 'technical_architecture' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="techArchitecture.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No technical architecture yet. Run the Technical Architecture Agent.</p>
            <p class="text-xs mt-1" v-if="businessRules.length === 0">Requires approved business rules first.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="suggestion in techArchitecture" 
              :key="suggestion.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge variant="outline">Architecture #{{ suggestion.id }}</Badge>
                <Badge :variant="suggestion.status === 'approved' ? 'default' : 'secondary'">
                  {{ suggestion.status }}
                </Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(suggestion.content)"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Quality & Tests -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">5️⃣</span>
                <span>Quality & Tests</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Test cases mapped to business rules</p>
            </div>
            <Button 
              @click="runAgent('quality_test')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'quality_test' || businessRules.length === 0"
            >
              {{ runningAgent === 'quality_test' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="tests.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No tests yet. Run the Quality & Test Agent.</p>
            <p class="text-xs mt-1" v-if="businessRules.length === 0">Requires approved business rules first.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="suggestion in tests" 
              :key="suggestion.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge variant="outline">Test Suite #{{ suggestion.id }}</Badge>
                <Badge :variant="suggestion.status === 'approved' ? 'default' : 'secondary'">
                  {{ suggestion.status }}
                </Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(suggestion.content)"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Change Impact & Drift -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">6️⃣</span>
                <span>Change Impact & Drift</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Impact analysis and drift detection</p>
            </div>
            <Button 
              @click="runAgent('change_impact')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'change_impact'"
            >
              {{ runningAgent === 'change_impact' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="changeImpacts.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No change impact analysis yet. Run the Change Impact Agent.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="impact in changeImpacts" 
              :key="impact.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge :variant="getRiskVariant(impact.risk_level)">{{ impact.change_type }}</Badge>
                <Badge variant="outline">{{ impact.risk_level }} risk</Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(impact.analysis_result)"></div>
              </div>
              <div v-if="impact.required_reruns" class="mt-3 text-xs text-gray-600">
                <strong>Required re-runs:</strong> {{ formatJsonArray(impact.required_reruns) }}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Release Readiness -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle class="flex items-center gap-2">
                <span class="text-2xl">7️⃣</span>
                <span>Release Readiness</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Release checklists and observability guidance</p>
            </div>
            <Button 
              @click="runAgent('release_readiness')" 
              variant="outline"
              size="sm"
              :disabled="runningAgent === 'release_readiness' || businessRules.length === 0"
            >
              {{ runningAgent === 'release_readiness' ? 'Running...' : 'Run Agent' }}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="releaseReadiness.length === 0" class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p>No release readiness checklist yet. Run the Release Readiness Agent.</p>
            <p class="text-xs mt-1" v-if="businessRules.length === 0">Requires approved business rules first.</p>
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="suggestion in releaseReadiness" 
              :key="suggestion.id"
              class="p-4 bg-gray-50 rounded-md border"
            >
              <div class="flex justify-between items-center mb-3">
                <Badge variant="outline">Release v{{ getReleaseVersion(suggestion) }}</Badge>
                <Badge :variant="suggestion.status === 'approved' ? 'default' : 'secondary'">
                  {{ suggestion.status }}
                </Badge>
              </div>
              <div class="prose prose-sm max-w-none">
                <div v-html="formatSuggestionContent(suggestion.content)"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Business Logic Input Dialog -->
    <Dialog :open="showBusinessLogicDialog" @update:open="showBusinessLogicDialog = $event">
      <DialogContent class="max-w-2xl">
        <DialogTitle>Describe Your Business Logic</DialogTitle>
        <div class="space-y-4 py-4">
          <p class="text-sm text-gray-600">
            Please describe your business logic, requirements, and policies. The AI will analyze your description and convert it into structured business rules with Rule IDs.
          </p>
          <div>
            <label class="block text-sm font-medium mb-2">Business Logic Description *</label>
            <Textarea 
              v-model="businessLogicText" 
              placeholder="Example: Our e-commerce platform allows customers to purchase items. Customers must be 18+ to make purchases. Orders over $100 get free shipping. Returns are accepted within 30 days of purchase..."
              rows="8"
              class="w-full"
            />
            <p class="text-xs text-gray-500 mt-2">
              Be as detailed as possible. Include policies, rules, edge cases, and any constraints.
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button @click="showBusinessLogicDialog = false" variant="secondary">Cancel</Button>
          <Button 
            @click="submitBusinessLogic" 
            variant="default"
            :disabled="!businessLogicText.trim() || runningAgent === 'business_logic_policy'"
          >
            {{ runningAgent === 'business_logic_policy' ? 'Processing...' : 'Generate Business Rules' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Run Agents Dialog -->
    <Dialog :open="showRunAgents" @update:open="showRunAgents = $event">
      <DialogContent>
        <DialogTitle>Run AI Agents</DialogTitle>
        <div class="space-y-4 py-4">
          <p class="text-sm text-gray-600">
            Select which agents to run. Agents will run in the correct order based on dependencies.
          </p>
          <div class="space-y-2">
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="business_logic_policy"
                class="rounded"
              />
              <span>1. Business Logic & Policy</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="product_requirements"
                class="rounded"
                :disabled="businessRules.length === 0"
              />
              <span>2. Product & Requirements</span>
              <span v-if="businessRules.length === 0" class="text-xs text-gray-400">(Requires business rules)</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="api_contract"
                class="rounded"
                :disabled="businessRules.length === 0"
              />
              <span>3. API & Contracts</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="technical_architecture"
                class="rounded"
                :disabled="businessRules.length === 0"
              />
              <span>4. Technical Architecture</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="quality_test"
                class="rounded"
                :disabled="businessRules.length === 0"
              />
              <span>5. Quality & Tests</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="change_impact"
                class="rounded"
              />
              <span>6. Change Impact & Drift</span>
            </label>
            <label class="flex items-center gap-2">
              <input 
                type="checkbox" 
                v-model="selectedAgents" 
                value="release_readiness"
                class="rounded"
                :disabled="businessRules.length === 0"
              />
              <span>7. Release Readiness</span>
            </label>
          </div>
        </div>
        <DialogFooter>
          <Button @click="showRunAgents = false" variant="secondary">Cancel</Button>
          <Button 
            @click="runAgentSequence" 
            variant="default"
            :disabled="selectedAgents.length === 0 || runningSequence"
          >
            {{ runningSequence ? 'Running...' : 'Run Selected Agents' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from './ui/dialog'
import { Textarea } from './ui/textarea'

export default {
  name: 'ProjectDetail',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Badge,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogFooter,
    Textarea
  },
  data() {
    return {
      projectId: null,
      runningAgent: null,
      runningSequence: false,
      showRunAgents: false,
      showBusinessLogicDialog: false,
      selectedAgents: [],
      businessLogicText: '',
      approvingRule: null
    }
  },
  computed: {
    ...mapState('projects', ['projects']),
    ...mapState('businessRules', ['rules']),
    ...mapState('suggestions', ['suggestions']),
    ...mapState('issues', ['issues']),
    ...mapState('changeImpacts', ['impacts']),
    project() {
      return this.projects.find(p => p.id === this.projectId)
    },
    businessRules() {
      if (!this.projectId) return []
      if (!this.rules || !Array.isArray(this.rules)) return []
      return this.rules.filter(r => r && (r.project_id === this.projectId || parseInt(r.project_id) === this.projectId))
    },
    productRequirements() {
      return this.getSuggestionsByAgent('product_requirements')
    },
    apiContracts() {
      return this.getSuggestionsByAgent('api_contract')
    },
    techArchitecture() {
      return this.getSuggestionsByAgent('technical_architecture')
    },
    tests() {
      return this.getSuggestionsByAgent('quality_test')
    },
    changeImpacts() {
      if (!this.projectId) return []
      return this.impacts.filter(i => i.project_id === this.projectId) || []
    },
    releaseReadiness() {
      return this.getSuggestionsByAgent('release_readiness')
    }
  },
  async mounted() {
    this.projectId = parseInt(this.$route.params.id)
    await this.fetchProjectData()
  },
  watch: {
    '$route.params.id'(newId) {
      this.projectId = parseInt(newId)
      this.fetchProjectData()
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjects']),
    ...mapActions('businessRules', ['fetchRules', 'approveRule']),
    ...mapActions('suggestions', ['fetchSuggestions']),
    ...mapActions('changeImpacts', ['fetchChangeImpacts']),
    async fetchProjectData() {
      try {
        await Promise.all([
          this.fetchProjects(),
          this.fetchRules(this.projectId),
          this.fetchSuggestions({ project_id: this.projectId }),
          this.fetchChangeImpacts(this.projectId)
        ])
      } catch (error) {
        console.error('Error fetching project data:', error)
      }
    },
    getSuggestionsByAgent(agentType) {
      if (!this.suggestions) return []
      return this.suggestions.filter(s => 
        s.agent_type === agentType && 
        s.project_id === this.projectId
      ) || []
    },
    handleBusinessLogicRun() {
      // If no business rules exist, show dialog to collect business logic description
      if (this.businessRules.length === 0) {
        this.showBusinessLogicDialog = true
      } else {
        // If rules exist, run agent directly (for updates)
        this.runAgent('business_logic_policy')
      }
    },
    async submitBusinessLogic() {
      if (!this.businessLogicText.trim()) {
        alert('Please provide a business logic description')
        return
      }
      
      this.showBusinessLogicDialog = false
      await this.runAgent('business_logic_policy')
      // Clear the text after submission
      this.businessLogicText = ''
    },
    async runAgent(agentType) {
      if (!this.projectId) return
      
      this.runningAgent = agentType
      try {
        const request = {
          project_id: this.projectId
        }

        if (agentType === 'business_logic_policy') {
          request.business_logic_text = this.businessLogicText || ''
        }

        await this.$store.dispatch('agents/runAgent', {
          agentType,
          request
        })
        
        // Refresh data - especially business rules after business logic agent runs
        await this.fetchProjectData()
        
        // If business logic agent ran successfully, show success message
        if (agentType === 'business_logic_policy') {
          // Clear the business logic text after successful submission
          this.businessLogicText = ''
        }
      } catch (error) {
        console.error('Failed to run agent:', error)
        alert('Failed to run agent: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.runningAgent = null
      }
    },
    async runAgentSequence() {
      if (this.selectedAgents.length === 0) return
      
      this.runningSequence = true
      try {
        await this.$store.dispatch('agents/runAgentSequence', {
          project_id: this.projectId,
          agent_types: this.selectedAgents
        })
        this.showRunAgents = false
        this.selectedAgents = []
        await this.fetchProjectData()
      } catch (error) {
        console.error('Failed to run agent sequence:', error)
        alert('Failed to run agents: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.runningSequence = false
      }
    },
    getStatusVariant(status) {
      const variants = {
        'approved': 'default',
        'pending_approval': 'secondary',
        'draft': 'outline'
      }
      return variants[status] || 'outline'
    },
    getRiskVariant(riskLevel) {
      const variants = {
        'critical': 'destructive',
        'high': 'destructive',
        'medium': 'secondary',
        'low': 'outline'
      }
      return variants[riskLevel] || 'outline'
    },
    formatSuggestionContent(content) {
      try {
        const parsed = JSON.parse(content)
        // Format JSON nicely
        return '<pre class="bg-white p-3 rounded border text-xs overflow-x-auto">' + 
               JSON.stringify(parsed, null, 2) + 
               '</pre>'
      } catch {
        // If not JSON, return as-is
        return '<div class="whitespace-pre-wrap text-sm">' + content + '</div>'
      }
    },
    getReleaseVersion(suggestion) {
      try {
        const parsed = JSON.parse(suggestion.content)
        return parsed.release_version || '1.0.0'
      } catch {
        return '1.0.0'
      }
    },
    formatJsonArray(jsonString) {
      try {
        const arr = JSON.parse(jsonString)
        return Array.isArray(arr) ? arr.join(', ') : jsonString
      } catch {
        return jsonString
      }
    },
    async approveRule(ruleId) {
      this.approvingRule = ruleId
      try {
        await this.$store.dispatch('businessRules/approveRule', {
          ruleId,
          approvedBy: 'user' // TODO: Get from auth context
        })
        await this.fetchRules(this.projectId)
      } catch (error) {
        console.error('Failed to approve rule:', error)
        alert('Failed to approve rule: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.approvingRule = null
      }
    },
    async rejectRule(ruleId) {
      if (!confirm('Are you sure you want to reject this rule? It will be marked as deprecated.')) {
        return
      }
      this.approvingRule = ruleId
      try {
        // Update rule status to deprecated
        await this.$store.dispatch('businessRules/updateRule', {
          ruleId,
          rule: { status: 'deprecated' }
        })
        await this.fetchRules(this.projectId)
      } catch (error) {
        console.error('Failed to reject rule:', error)
        alert('Failed to reject rule: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.approvingRule = null
      }
    },
    formatAssumptions(assumptions) {
      if (!assumptions) return 'None'
      try {
        const parsed = JSON.parse(assumptions)
        if (Array.isArray(parsed)) {
          return parsed.join(', ')
        }
        return String(parsed)
      } catch {
        return String(assumptions)
      }
    }
  }
}
</script>

<style scoped>
.project-detail {
  padding: 2rem 0;
}
</style>
