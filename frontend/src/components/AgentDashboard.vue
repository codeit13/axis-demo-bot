<template>
  <div class="dashboard">
    <h2 class="text-3xl font-bold mb-2">Agent Dashboard</h2>
    <p class="text-gray-600 mb-8">Manage and run AI agents for your development workflow</p>

    <div v-if="productionAgents.length > 0" class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Production Agents</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card v-for="agent in productionAgents" :key="agent.value" class="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle class="text-purple-600">{{ agent.name }}</CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-gray-600 text-sm mb-4 min-h-[3rem]">
              {{ agentDescriptions[agent.value] || 'AI agent for development workflow' }}
            </p>
            <div class="space-y-2">
              <Select 
                :modelValue="selectedProjects[agent.value] || undefined" 
                @update:modelValue="updateSelectedProject(agent.value, $event)"
              >
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select Project" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="project in projects" :key="project.id" :value="String(project.id)">
                    {{ project.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <div v-if="agent.value === 'business_logic_policy'" class="space-y-2">
                <Textarea
                  v-model="businessLogicText[agent.value]"
                  placeholder="Enter business logic description..."
                  class="w-full"
                  rows="3"
                />
              </div>
              <Button 
                @click="handleRunAgent(agent.value)" 
                variant="default"
                class="w-full"
                :disabled="!selectedProjects[agent.value] || isAgentLoading(agent.value)"
              >
                {{ isAgentLoading(agent.value) ? 'Running...' : 'Run Agent' }}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <div v-if="legacyAgents.length > 0" class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Legacy Agents</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card v-for="agent in legacyAgents" :key="agent.value" class="hover:shadow-lg transition-shadow opacity-75">
          <CardHeader>
            <CardTitle class="text-gray-500">{{ agent.name }}</CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-gray-600 text-sm mb-4 min-h-[3rem]">
              {{ agentDescriptions[agent.value] || 'Legacy agent' }}
            </p>
            <div class="space-y-2">
              <Select 
                :modelValue="selectedProjects[agent.value] || undefined" 
                @update:modelValue="updateSelectedProject(agent.value, $event)"
              >
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select Project" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="project in projects" :key="project.id" :value="String(project.id)">
                    {{ project.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <Button 
                @click="handleRunAgent(agent.value)" 
                variant="secondary"
                class="w-full"
                :disabled="!selectedProjects[agent.value] || isAgentLoading(agent.value)"
              >
                {{ isAgentLoading(agent.value) ? 'Running...' : 'Run Agent' }}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <Card v-if="lastResult" class="mt-8">
      <CardHeader>
        <CardTitle>Last Result</CardTitle>
      </CardHeader>
      <CardContent>
        <div v-if="lastResult.status === 'success'" class="bg-green-50 text-green-800 p-4 rounded-md">
          ✓ {{ lastResult.message }}
        </div>
        <div v-else class="bg-red-50 text-red-800 p-4 rounded-md">
          ✗ {{ lastResult.error || 'An error occurred' }}
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Textarea } from './ui/textarea'

export default {
  name: 'AgentDashboard',
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
    Textarea
  },
  data() {
    return {
      selectedProjects: {},
      businessLogicText: {},
      showBusinessLogicInput: {}
    }
  },
  computed: {
    ...mapState('projects', ['projects']),
    ...mapState('agents', ['lastResult', 'agentTypes']),
    ...mapGetters('agents', ['isAgentLoading', 'productionAgents', 'legacyAgents']),
    agents() {
      return this.agentTypes || []
    },
    agentDescriptions() {
      return {
        'business_logic_policy': 'Canonical source for business rules with versioning and Rule IDs',
        'product_requirements': 'Translates business logic into product requirements',
        'api_contract': 'Defines system contracts (OpenAPI/gRPC) with Rule ID annotation',
        'technical_architecture': 'Technical design without code generation',
        'quality_test': 'Validates correctness against business intent',
        'change_impact': 'Prevents silent breakage through impact analysis',
        'release_readiness': 'Production safety with checklists and observability'
      }
    }
  },
  async mounted() {
    await this.fetchProjects()
    await this.fetchAgentTypes()
  },
  methods: {
    ...mapActions('projects', ['fetchProjects']),
    ...mapActions('agents', ['fetchAgentTypes', 'runAgent']),
    updateSelectedProject(agentValue, projectId) {
      // Convert to number if it's a numeric string, handle undefined/null
      const id = !projectId || projectId === '' ? null : (isNaN(projectId) ? projectId : Number(projectId))
      this.selectedProjects[agentValue] = id
    },
    async handleRunAgent(agentType) {
      const projectId = this.selectedProjects[agentType]
      if (!projectId) return

      try {
        const request = {
          project_id: projectId,
          additional_params: {}
        }

        // Add agent-specific parameters
        if (agentType === 'business_logic_policy') {
          request.business_logic_text = this.businessLogicText[agentType] || ''
        }

        const result = await this.runAgent({
          agentType,
          request
        })
        if (result?.status === 'success') {
          this.$router.push('/suggestions')
        }
      } catch (error) {
        console.error('Failed to run agent:', error)
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem 0;
}
</style>
