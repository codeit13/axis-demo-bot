<template>
  <div class="bug-scanner">
    <h2 class="text-3xl font-bold mb-2">Bug Scanner</h2>
    <p class="text-gray-600 mb-8">Report bugs and get AI-suggested fixes</p>

    <div class="space-y-6">
      <!-- Report Bug Section -->
      <Card>
        <CardHeader>
          <CardTitle>Report a Bug</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Select Project</label>
              <Select v-model="bugReport.project_id">
                <SelectTrigger>
                  <SelectValue placeholder="Select Project" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="project in projects" :key="project.id" :value="String(project.id)">
                    {{ project.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Bug Title</label>
              <Input v-model="bugReport.title" placeholder="Brief description of the bug" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Bug Description</label>
              <Textarea 
                v-model="bugReport.description" 
                placeholder="Detailed description of the bug, steps to reproduce, expected vs actual behavior..."
                class="min-h-[120px]"
              />
            </div>
            <Button 
              @click="reportBug" 
              variant="default"
              :disabled="!bugReport.project_id || !bugReport.title || loading"
            >
              {{ loading ? 'Creating...' : 'Report Bug & Get Fix Suggestion' }}
            </Button>
          </div>
        </CardContent>
      </Card>

      <!-- Scan Codebase Section -->
      <Card>
        <CardHeader>
          <CardTitle>Scan Codebase for Bugs</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Select Project</label>
              <Select v-model="scanProjectId">
                <SelectTrigger>
                  <SelectValue placeholder="Select Project" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="project in projects" :key="project.id" :value="String(project.id)">
                    {{ project.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button 
              @click="scanCodebase" 
              variant="default"
              :disabled="!scanProjectId || scanning"
            >
              {{ scanning ? 'Scanning...' : 'Scan Codebase' }}
            </Button>
          </div>
        </CardContent>
      </Card>

      <!-- Issues List -->
      <Card>
        <CardHeader>
          <CardTitle>Issues</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Filter by Project</label>
            <Select v-model="issueFilterProjectId" @update:modelValue="issueFilterProjectId = $event || null; loadIssues()">
              <SelectTrigger>
                <SelectValue placeholder="All Projects" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="project in projects" :key="project.id" :value="String(project.id)">
                  {{ project.name }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div v-if="issues.length === 0" class="text-center py-12 text-gray-500">
            <p>No issues found. Report a bug or scan your codebase to get started.</p>
          </div>

          <div v-for="issue in issues" :key="issue.id" class="bg-gray-50 p-4 rounded-md mb-4 border-l-4 border-purple-500">
            <div class="flex justify-between items-start mb-2">
              <div class="flex items-center gap-2 flex-wrap">
                <h4 class="font-semibold">{{ issue.title }}</h4>
                <Badge :variant="issue.status">{{ issue.status }}</Badge>
                <Badge v-if="issue.bitbucket_issue_id" variant="secondary" class="bg-blue-100 text-blue-800">
                  Bitbucket: {{ issue.bitbucket_issue_id }}
                </Badge>
              </div>
              <Button 
                @click="getFixSuggestion(issue.id)" 
                variant="default"
                :disabled="loadingFix === issue.id"
              >
                {{ loadingFix === issue.id ? 'Generating...' : 'Get Fix Suggestion' }}
              </Button>
            </div>
            <div class="text-gray-700 mb-2">
              <p>{{ issue.description }}</p>
            </div>
            <div class="text-sm text-gray-500">
              Created: {{ formatDate(issue.created_at) }}
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Fix Suggestion Dialog -->
      <Dialog :open="!!selectedFix" @update:open="selectedFix = null">
        <DialogTitle>Fix Suggestion</DialogTitle>
        <DialogContent>
          <div class="space-y-4">
            <div v-if="fixData.bug_explanation">
              <h4 class="font-semibold mb-2 text-purple-600">Bug Explanation</h4>
              <p class="text-gray-700">{{ fixData.bug_explanation }}</p>
            </div>
            <div v-if="fixData.root_cause">
              <h4 class="font-semibold mb-2 text-purple-600">Root Cause</h4>
              <p class="text-gray-700">{{ fixData.root_cause }}</p>
            </div>
            <div v-if="fixData.suggested_fix">
              <h4 class="font-semibold mb-2 text-purple-600">Suggested Fix</h4>
              <div class="bg-gray-50 p-4 rounded border overflow-x-auto">
                <pre class="text-sm"><code>{{ fixData.suggested_fix }}</code></pre>
              </div>
            </div>
            <div v-if="fixData.unit_tests">
              <h4 class="font-semibold mb-2 text-purple-600">Unit Tests</h4>
              <div class="bg-gray-50 p-4 rounded border overflow-x-auto">
                <pre class="text-sm"><code>{{ fixData.unit_tests }}</code></pre>
              </div>
            </div>
          </div>
        </DialogContent>
        <DialogFooter>
          <Button @click="approveFix" variant="default" class="bg-green-600 hover:bg-green-700">Approve Fix</Button>
          <Button @click="selectedFix = null" variant="secondary">Close</Button>
        </DialogFooter>
      </Dialog>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Badge } from './ui/badge'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from './ui/dialog'

export default {
  name: 'BugScanner',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Input,
    Textarea,
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
      bugReport: {
        project_id: '',
        title: '',
        description: ''
      },
      scanProjectId: '',
      issueFilterProjectId: '',
      loading: false,
      scanning: false,
      loadingFix: null,
      selectedFix: null,
      fixData: {}
    }
  },
  computed: {
    ...mapState('projects', ['projects']),
    ...mapState('issues', ['issues', 'loading']),
    ...mapState('suggestions', ['suggestions'])
  },
  async mounted() {
    await this.fetchProjects()
    await this.loadIssues()
  },
  methods: {
    ...mapActions('projects', ['fetchProjects']),
    ...mapActions('issues', ['createIssue', 'fetchIssuesByProject', 'setFilterProjectId']),
    ...mapActions('agents', ['runAgent']),
    ...mapActions('suggestions', ['fetchSuggestions', 'approveSuggestion']),
    async reportBug() {
      if (!this.bugReport.project_id || !this.bugReport.title) return

      this.loading = true
      try {
        const issue = await this.$store.dispatch('issues/createIssue', {
          projectId: this.bugReport.project_id,
          issueData: {
            title: this.bugReport.title,
            description: this.bugReport.description
          }
        })

        await this.getFixSuggestion(issue.id)

        this.bugReport = { project_id: '', title: '', description: '' }
        await this.loadIssues()
      } catch (error) {
        alert('Failed to report bug: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loading = false
      }
    },
    async scanCodebase() {
      if (!this.scanProjectId) return

      this.scanning = true
      try {
        await this.$store.dispatch('agents/runAgent', {
          agentType: 'bug_scanner',
          request: {
            project_id: this.scanProjectId,
            additional_params: { scan_all: true }
          }
        })
        await this.loadIssues()
        alert('Codebase scan completed! Check issues for found bugs.')
      } catch (error) {
        alert('Failed to scan codebase: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.scanning = false
      }
    },
    async getFixSuggestion(issueId) {
      this.loadingFix = issueId
      try {
        const issue = this.issues.find(i => i.id === issueId)
        if (!issue) return

        await this.$store.dispatch('agents/runAgent', {
          agentType: 'bug_scanner',
          request: {
            project_id: issue.project_id,
            issue_id: issueId
          }
        })
        
        await this.$store.dispatch('suggestions/fetchSuggestions')
        const suggestion = this.suggestions.find(s => s.issue_id === issueId)
        
        if (suggestion) {
          try {
            this.fixData = JSON.parse(suggestion.content)
          } catch {
            this.fixData = { suggested_fix: suggestion.content }
          }
          this.selectedFix = suggestion
        } else {
          alert('Fix suggestion is being generated. Please check back in a moment.')
        }
      } catch (error) {
        alert('Failed to get fix suggestion: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loadingFix = null
      }
    },
    async approveFix() {
      if (!this.selectedFix) return

      try {
        await this.$store.dispatch('suggestions/approveSuggestion', {
          suggestionId: this.selectedFix.id,
          action: 'approve',
          comments: 'Fix approved'
        })
        this.selectedFix = null
        this.$router.push('/suggestions')
      } catch (error) {
        alert('Failed to approve fix: ' + (error.response?.data?.detail || error.message))
      }
    },
    async loadIssues() {
      if (this.issueFilterProjectId) {
        await this.fetchIssuesByProject(this.issueFilterProjectId)
      } else {
        this.setFilterProjectId(null)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.bug-scanner {
  padding: 2rem 0;
}
</style>
