<template>
  <div class="business-logic-manager">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-3xl font-bold mb-2">Business Rules</h2>
        <p class="text-gray-600">Manage versioned business rules with Rule IDs</p>
      </div>
      <Button @click="showCreateDialog = true" variant="default">
        Create Rule
      </Button>
    </div>

    <!-- Project Selector -->
    <Card class="mb-6">
      <CardContent class="pt-6">
        <Select 
          :modelValue="selectedProjectId || undefined" 
          @update:modelValue="selectedProjectId = $event || null"
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
      </CardContent>
    </Card>

    <!-- Rules List -->
    <div v-if="selectedProjectId && rules.length > 0" class="space-y-4">
      <Card v-for="rule in rules" :key="rule.rule_id" class="hover:shadow-lg transition-shadow">
        <CardHeader>
          <div class="flex justify-between items-start">
            <div>
              <CardTitle class="flex items-center gap-2">
                <Badge :variant="getStatusVariant(rule.status)">{{ rule.rule_id }}</Badge>
                <span class="text-lg">{{ rule.status }}</span>
              </CardTitle>
              <p class="text-sm text-gray-500 mt-1">Version: {{ rule.version }}</p>
            </div>
            <div class="flex gap-2">
              <Button 
                v-if="rule.status === 'pending_approval'" 
                @click="approveRule(rule.rule_id)"
                variant="default"
                size="sm"
              >
                Approve
              </Button>
              <Button 
                @click="viewVersions(rule.rule_id)"
                variant="secondary"
                size="sm"
              >
                View Versions
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <p class="text-gray-700 whitespace-pre-wrap">{{ rule.content }}</p>
          <div v-if="rule.assumptions" class="mt-4 p-3 bg-gray-50 rounded">
            <p class="text-sm font-semibold mb-1">Assumptions:</p>
            <p class="text-sm text-gray-600">{{ rule.assumptions }}</p>
          </div>
          <div class="mt-4 text-xs text-gray-500">
            Created by: {{ rule.created_by }} | 
            <span v-if="rule.approved_by">Approved by: {{ rule.approved_by }}</span>
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else-if="selectedProjectId && rules.length === 0" class="text-center py-12 text-gray-500">
      No business rules found. Create your first rule!
    </div>

    <!-- Create Rule Dialog -->
    <Dialog :open="showCreateDialog" @update:open="showCreateDialog = $event">
      <DialogContent>
        <DialogTitle>Create Business Rule</DialogTitle>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Business Logic Description</label>
            <Textarea
              v-model="newRuleContent"
              placeholder="Enter business logic description..."
              rows="6"
              class="w-full"
            />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Assumptions (optional)</label>
            <Textarea
              v-model="newRuleAssumptions"
              placeholder="Enter explicit assumptions..."
              rows="3"
              class="w-full"
            />
          </div>
        </div>
        <DialogFooter>
          <Button @click="showCreateDialog = false" variant="secondary">Cancel</Button>
          <Button @click="createRule" variant="default" :disabled="!newRuleContent || !selectedProjectId">
            Create Rule
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Versions Dialog -->
    <Dialog :open="showVersionsDialog" @update:open="showVersionsDialog = $event">
      <DialogContent class="max-w-3xl">
        <DialogTitle>Version History: {{ currentRuleId }}</DialogTitle>
        <div class="space-y-4 max-h-96 overflow-y-auto">
          <Card v-for="version in ruleVersions" :key="version.id">
            <CardHeader>
              <CardTitle class="text-sm">Version {{ version.version }}</CardTitle>
              <p class="text-xs text-gray-500">{{ version.created_at }}</p>
            </CardHeader>
            <CardContent>
              <p class="text-sm whitespace-pre-wrap">{{ version.content }}</p>
              <div v-if="version.diff" class="mt-3 p-2 bg-gray-50 rounded text-xs">
                <p class="font-semibold mb-1">Changes:</p>
                <p class="text-gray-600">{{ version.diff }}</p>
              </div>
            </CardContent>
          </Card>
        </div>
        <DialogFooter>
          <Button @click="showVersionsDialog = false" variant="secondary">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Textarea } from './ui/textarea'
import { Badge } from './ui/badge'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from './ui/dialog'

export default {
  name: 'BusinessLogicManager',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Select,
    Textarea,
    Badge,
    Dialog,
    DialogContent,
    DialogTitle,
    DialogFooter
  },
  data() {
    return {
      selectedProjectId: null,
      showCreateDialog: false,
      showVersionsDialog: false,
      newRuleContent: '',
      newRuleAssumptions: '',
      currentRuleId: '',
      ruleVersions: []
    }
  },
  computed: {
    ...mapState('projects', ['projects']),
    ...mapState('businessRules', ['rules', 'loading'])
  },
  watch: {
    selectedProjectId(newId) {
      if (newId) {
        this.fetchRulesAction(newId)
      }
    }
  },
  async mounted() {
    await this.fetchProjects()
  },
  methods: {
    ...mapActions('projects', ['fetchProjects']),
    ...mapActions('businessRules', {
      fetchRulesAction: 'fetchRules',
      createRuleAction: 'createRule',
      approveRuleAction: 'approveRule',
      fetchRuleVersionsAction: 'fetchRuleVersions'
    }),
    getStatusVariant(status) {
      const variants = {
        'approved': 'default',
        'pending_approval': 'secondary',
        'draft': 'outline'
      }
      return variants[status] || 'outline'
    },
    async createRule() {
      if (!this.newRuleContent || !this.selectedProjectId) return
      try {
        await this.createRuleAction({
          projectId: this.selectedProjectId,
          rule: {
            content: this.newRuleContent,
            assumptions: this.newRuleAssumptions || null,
            created_by: 'user'
          }
        })
        this.showCreateDialog = false
        this.newRuleContent = ''
        this.newRuleAssumptions = ''
        await this.fetchRulesAction(this.selectedProjectId)
      } catch (error) {
        console.error('Failed to create rule:', error)
      }
    },
    async approveRule(ruleId) {
      try {
        await this.approveRuleAction({
          ruleId,
          approvedBy: 'user'
        })
        await this.fetchRulesAction(this.selectedProjectId)
      } catch (error) {
        console.error('Failed to approve rule:', error)
      }
    },
    async viewVersions(ruleId) {
      this.currentRuleId = ruleId
      try {
        const versions = await this.fetchRuleVersionsAction(ruleId)
        this.ruleVersions = versions
        this.showVersionsDialog = true
      } catch (error) {
        console.error('Failed to fetch versions:', error)
      }
    }
  }
}
</script>

<style scoped>
.business-logic-manager {
  padding: 2rem 0;
}
</style>
