<template>
  <div class="project-manager">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h2 class="text-3xl font-bold mb-2">Project Manager</h2>
        <p class="text-gray-600">Create and manage your projects. Codebase is optional and can be added later.</p>
      </div>
      <Button @click="showCreateProject = true" variant="default">Create Project</Button>
    </div>

    <!-- Create Project Dialog -->
    <Dialog :open="showCreateProject" @update:open="showCreateProject = $event">
      <DialogContent class="max-w-2xl">
        <DialogTitle>Create New Project</DialogTitle>
        <div class="space-y-6 py-4">
          <!-- Basic Info -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Project Name *</label>
              <Input v-model="newProject.name" placeholder="My Project" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Description</label>
              <Textarea 
                v-model="newProject.description" 
                placeholder="Project description" 
                rows="3"
              />
            </div>
          </div>

          <!-- Codebase Source (Optional) -->
          <div class="space-y-4 border-t pt-4">
            <div>
              <label class="block text-sm font-medium mb-2">
                Codebase Source <span class="text-gray-500 font-normal">(Optional)</span>
              </label>
              <p class="text-xs text-gray-500 mb-3">
                You can add codebase later. The first 4 agents (Business Logic, Product Requirements, APIs & Contracts, Architecture) will work without codebase.
              </p>
              
              <!-- Toggle between GitHub URL and ZIP Upload -->
              <div class="flex gap-2 mb-4">
                <Button
                  @click="codebaseSource = 'github'"
                  :variant="codebaseSource === 'github' ? 'default' : 'outline'"
                  size="sm"
                >
                  GitHub URL
                </Button>
                <Button
                  @click="codebaseSource = 'zip'"
                  :variant="codebaseSource === 'zip' ? 'default' : 'outline'"
                  size="sm"
                >
                  Upload ZIP
                </Button>
                <Button
                  @click="codebaseSource = null"
                  :variant="codebaseSource === null ? 'default' : 'outline'"
                  size="sm"
                >
                  Skip for Now
                </Button>
              </div>

              <!-- GitHub URL Input -->
              <div v-if="codebaseSource === 'github'" class="space-y-2">
                <Input 
                  v-model="newProject.repository_url" 
                  placeholder="https://github.com/username/repo" 
                />
                <p class="text-xs text-gray-500">
                  Enter your GitHub repository URL. We'll fetch the codebase from there.
                </p>
              </div>

              <!-- ZIP Upload -->
              <div v-if="codebaseSource === 'zip'" class="space-y-2">
                <div class="flex items-center gap-4">
                  <label 
                    for="zip-upload" 
                    class="cursor-pointer inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2"
                  >
                    Choose ZIP File
                  </label>
                  <input
                    id="zip-upload"
                    type="file"
                    accept=".zip"
                    @change="handleZipUpload"
                    class="hidden"
                  />
                  <span v-if="zipFileName" class="text-sm text-gray-600">{{ zipFileName }}</span>
                </div>
                <p class="text-xs text-gray-500">
                  Upload a ZIP file containing your codebase. Maximum size: 50MB
                </p>
              </div>
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button @click="showCreateProject = false" variant="secondary">Cancel</Button>
          <Button 
            @click="handleCreateProject" 
            variant="default"
            :disabled="!newProject.name || creating"
          >
            {{ creating ? 'Creating...' : 'Create Project' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Projects List -->
    <div v-if="projects.length === 0 && !loading" class="text-center py-12">
      <p class="text-gray-500 mb-4">No projects yet. Create your first project to get started!</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Loading projects...</p>
    </div>

    <div v-if="projects.length > 0" class="space-y-4">
      <Card v-for="project in projects" :key="project.id" class="hover:shadow-md transition-shadow">
        <CardHeader>
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <CardTitle class="text-xl mb-2">{{ project.name }}</CardTitle>
              <p class="text-gray-600 mb-3">{{ project.description || 'No description' }}</p>
              <div class="flex gap-4 text-sm text-gray-500">
                <span v-if="project.repository_url" class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                  {{ project.repository_url }}
                </span>
                <span v-if="project.business_logic_version" class="flex items-center gap-1">
                  <Badge variant="outline">BL v{{ project.business_logic_version }}</Badge>
                </span>
              </div>
            </div>
            <div class="flex gap-2 ml-4">
              <Button 
                @click="toggleProjectFiles(project.id)" 
                variant="secondary"
                size="sm"
              >
                {{ expandedProjects[project.id] ? 'Hide' : 'Show' }} Files
              </Button>
              <Button 
                @click="showAddFile(project.id)" 
                variant="default"
                size="sm"
              >
                Add File
              </Button>
            </div>
          </div>
        </CardHeader>

        <!-- Files List -->
        <CardContent v-if="expandedProjects[project.id]">
          <div v-if="!projectFiles[project.id] || projectFiles[project.id].length === 0" 
               class="text-center py-8 text-gray-500 border border-dashed rounded-md">
            <p class="mb-2">No code files yet.</p>
            <p class="text-sm">Add code files manually or upload a ZIP file to get started.</p>
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="file in projectFiles[project.id]" 
              :key="file.id" 
              class="bg-gray-50 p-4 rounded-md border"
            >
              <div class="flex justify-between items-center mb-2">
                <span class="font-mono text-sm font-medium">{{ file.file_path }}</span>
                <Badge variant="secondary">{{ file.language || 'Unknown' }}</Badge>
              </div>
              <div class="bg-white p-3 rounded border text-xs overflow-x-auto">
                <pre class="whitespace-pre-wrap"><code>{{ file.content.substring(0, 300) }}{{ file.content.length > 300 ? '...' : '' }}</code></pre>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Add File Dialog -->
    <Dialog :open="showAddFileModal !== null" @update:open="showAddFileModal = $event ? showAddFileModal : null">
      <DialogContent>
        <DialogTitle>Add Code File</DialogTitle>
        <div class="space-y-4 py-4">
          <div>
            <label class="block text-sm font-medium mb-2">File Path *</label>
            <Input v-model="newFile.file_path" placeholder="src/main.py" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Language</label>
            <Input v-model="newFile.language" placeholder="python" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Code Content *</label>
            <Textarea 
              v-model="newFile.content" 
              placeholder="Your code here..." 
              class="min-h-[200px] font-mono text-sm"
            />
          </div>
        </div>
        <DialogFooter>
          <Button @click="showAddFileModal = null" variant="secondary">Cancel</Button>
          <Button 
            @click="addFile(showAddFileModal)" 
            variant="default"
            :disabled="!newFile.file_path || !newFile.content || addingFile"
          >
            {{ addingFile ? 'Adding...' : 'Add File' }}
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
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from './ui/dialog'
import { Badge } from './ui/badge'

export default {
  name: 'ProjectManager',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button,
    Input,
    Textarea,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogFooter,
    Badge
  },
  data() {
    return {
      expandedProjects: {},
      showCreateProject: false,
      showAddFileModal: null,
      creating: false,
      addingFile: false,
      codebaseSource: null, // 'github', 'zip', or null
      zipFileName: null,
      zipFile: null,
      newProject: {
        name: '',
        description: '',
        repository_url: ''
      },
      newFile: {
        file_path: '',
        language: '',
        content: ''
      }
    }
  },
  computed: {
    ...mapState('projects', ['projects', 'codeFiles', 'loading']),
    projectFiles() {
      return this.codeFiles || {}
    }
  },
  async mounted() {
    await this.fetchProjects()
  },
  methods: {
    ...mapActions('projects', ['fetchProjects', 'createProject', 'fetchCodeFiles', 'createCodeFile']),
    handleZipUpload(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 50 * 1024 * 1024) {
          alert('File size exceeds 50MB limit')
          event.target.value = ''
          return
        }
        this.zipFile = file
        this.zipFileName = file.name
      }
    },
    async handleCreateProject() {
      if (!this.newProject.name) {
        alert('Project name is required')
        return
      }

      this.creating = true
      try {
        const projectData = {
          name: this.newProject.name,
          description: this.newProject.description || null,
          repository_url: this.codebaseSource === 'github' ? (this.newProject.repository_url || null) : null
        }

        const project = await this.createProject(projectData)

        // If ZIP file was uploaded, handle it
        if (this.codebaseSource === 'zip' && this.zipFile) {
          // TODO: Implement ZIP file upload and extraction
          // For now, just show a message
          console.log('ZIP upload would be processed here', this.zipFile)
          alert('ZIP file upload will be processed. For now, you can add files manually.')
        }

        // Reset form
        this.showCreateProject = false
        this.newProject = { name: '', description: '', repository_url: '' }
        this.codebaseSource = null
        this.zipFileName = null
        this.zipFile = null
      } catch (error) {
        alert('Failed to create project: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.creating = false
      }
    },
    showAddFile(projectId) {
      this.showAddFileModal = projectId
      this.newFile = { file_path: '', language: '', content: '' }
    },
    async addFile(projectId) {
      if (!this.newFile.file_path || !this.newFile.content) {
        alert('File path and content are required')
        return
      }

      this.addingFile = true
      try {
        await this.$store.dispatch('projects/createCodeFile', {
          projectId,
          fileData: this.newFile
        })
        this.showAddFileModal = null
        this.newFile = { file_path: '', language: '', content: '' }
      } catch (error) {
        alert('Failed to add file: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.addingFile = false
      }
    },
    async toggleProjectFiles(projectId) {
      this.expandedProjects[projectId] = !this.expandedProjects[projectId]
      if (this.expandedProjects[projectId] && !this.projectFiles[projectId]) {
        await this.fetchCodeFiles(projectId)
      }
    }
  }
}
</script>

<style scoped>
.project-manager {
  padding: 2rem 0;
}
</style>
