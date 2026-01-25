<template>
  <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-6xl max-h-[90vh] overflow-y-auto border-0">
      <!-- Header -->
      <div class="dialog-header-gradient">
        <div class="dialog-header-content">
          <div class="flex items-center gap-3">
            <div class="header-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>
            <div>
              <DialogTitle class="header-title">Code Template Library</DialogTitle>
              <p class="header-subtitle">Production-ready microservice templates with best practices</p>
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

      <!-- Navigation Tabs -->
      <div class="tabs-container">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Templates Grid -->
      <div class="templates-content">
        <div class="templates-grid">
          <Card 
            v-for="template in filteredTemplates" 
            :key="template.id"
            class="template-card"
          >
            <CardContent class="template-card-content">
              <div class="template-header">
                <div class="template-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                    <line x1="3" y1="9" x2="21" y2="9"></line>
                    <line x1="3" y1="15" x2="21" y2="15"></line>
                  </svg>
                </div>
                <Badge :variant="getBadgeVariant(template.type)" class="template-badge">
                  {{ template.type }}
                </Badge>
              </div>
              
              <h3 class="template-title">{{ template.title }}</h3>
              <p class="template-description">{{ template.description }}</p>
              
              <div class="technologies-section">
                <div class="technologies-tags">
                  <span 
                    v-for="tech in template.technologies" 
                    :key="tech"
                    class="tech-tag"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>
              
              <div class="features-section">
                <div class="features-title">Features:</div>
                <ul class="features-list">
                  <li v-for="feature in template.features" :key="feature">
                    {{ feature }}
                  </li>
                </ul>
              </div>
              
              <Button variant="default" class="use-template-button" @click="useTemplate(template)">
                Use Template
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- Footer -->
      <div class="dialog-footer">
        <div class="footer-info">
          {{ filteredTemplates.length }} Templates Available • All templates follow Axis Bank coding standards
        </div>
        <Button variant="outline" class="close-footer-button" @click="$emit('update:open', false)">
          Close
        </Button>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { Dialog, DialogContent, DialogTitle, DialogClose } from './ui/dialog'
import { Button } from './ui/button'
import { Card, CardContent } from './ui/card'
import { Badge } from './ui/badge'

export default {
  name: 'CodeTemplateAgentDialog',
  components: {
    Dialog,
    DialogContent,
    DialogTitle,
    DialogClose,
    Button,
    Card,
    CardContent,
    Badge
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
      activeTab: 'all',
      loading: false,
      tabs: [
        { id: 'all', label: 'All Templates' },
        { id: 'rest', label: 'REST APIs' },
        { id: 'messaging', label: 'Messaging' },
        { id: 'websocket', label: 'WebSocket' }
      ],
      templates: [
        {
          id: 1,
          title: 'Authentication Service',
          type: 'REST API',
          description: 'Complete JWT-based authentication with user management',
          technologies: ['TypeScript', 'Node.js', 'PostgreSQL'],
          features: ['JWT Tokens', 'Password Hashing', 'Role-Based Access']
        },
        {
          id: 2,
          title: 'CRUD API',
          type: 'REST API',
          description: 'Standard RESTful CRUD operations with database integration',
          technologies: ['Python', 'FastAPI', 'SQLAlchemy'],
          features: ['SQLAlchemy', 'Pydantic Models', 'Auto-Documentation']
        },
        {
          id: 3,
          title: 'Event-Driven Service',
          type: 'Message Queue',
          description: 'Microservice with message queue integration',
          technologies: ['Go', 'RabbitMQ', 'MongoDB'],
          features: ['RabbitMQ', 'Event Handlers', 'Dead Letter Queue']
        },
        {
          id: 4,
          title: 'Real-time Chat',
          type: 'WebSocket',
          description: 'WebSocket-based chat service with room support',
          technologies: ['TypeScript', 'Socket.io', 'Redis'],
          features: ['Socket.io', 'Room Management', 'Message History']
        },
        {
          id: 5,
          title: 'File Upload Service',
          type: 'REST API',
          description: 'Handle file uploads with cloud storage integration',
          technologies: ['Java', 'Spring Boot', 'AWS S3'],
          features: ['S3 Integration', 'File Validation', 'Streaming Upload']
        },
        {
          id: 6,
          title: 'Payment Gateway',
          type: 'REST API',
          description: 'Payment processing with Stripe integration',
          technologies: ['TypeScript', 'Node.js', 'Stripe'],
          features: ['Stripe API', 'Webhooks', 'Refund Handling']
        }
      ]
    }
  },
  computed: {
    filteredTemplates() {
      if (this.activeTab === 'all') {
        return this.templates
      } else if (this.activeTab === 'rest') {
        return this.templates.filter(t => t.type === 'REST API')
      } else if (this.activeTab === 'messaging') {
        return this.templates.filter(t => t.type === 'Message Queue')
      } else if (this.activeTab === 'websocket') {
        return this.templates.filter(t => t.type === 'WebSocket')
      }
      return this.templates
    }
  },
  async mounted() {
    // Fetch templates from backend
    await this.loadTemplates()
  },
  methods: {
    ...mapActions('projects', ['fetchProjects', 'createProject']),
    ...mapActions('agents', ['runAgent']),
    async loadTemplates() {
      this.loading = true
      try {
        const projects = await this.fetchProjects()
        let projectId = projects && projects.length > 0 ? projects[0].id : null
        
        if (!projectId) {
          const newProject = await this.createProject({
            name: 'Code Template Agent Demo',
            description: 'Demo project for Code Template Agent'
          })
          projectId = newProject.id
        }
        
        const result = await this.runAgent({
          agentType: 'code_template_agent',
          request: {
            project_id: projectId
          }
        })
        
        if (result.status === 'success' && result.templates) {
          this.templates = result.templates.map((t, index) => ({
            id: index + 1,
            title: t.title,
            type: t.type,
            description: t.description,
            technologies: t.technologies,
            features: t.features
          }))
        }
      } catch (error) {
        console.error('Error loading templates:', error)
        // Keep default templates on error
      } finally {
        this.loading = false
      }
    },
    getBadgeVariant(type) {
      if (type === 'REST API') return 'default'
      if (type === 'Message Queue') return 'secondary'
      if (type === 'WebSocket') return 'outline'
      return 'default'
    },
    async useTemplate(template) {
      try {
        const projects = await this.fetchProjects()
        let projectId = projects && projects.length > 0 ? projects[0].id : null
        
        if (!projectId) {
          const newProject = await this.createProject({
            name: 'Code Template Agent Demo',
            description: 'Demo project for Code Template Agent'
          })
          projectId = newProject.id
        }
        
        const result = await this.runAgent({
          agentType: 'code_template_agent',
          request: {
            project_id: projectId,
            template_type: template.id,
            service_name: template.title,
            technologies: template.technologies
          }
        })
        
        if (result.status === 'success') {
          alert(`Template "${template.title}" has been generated! Check the suggestions for the complete code.`)
        } else {
          alert('Failed to generate template: ' + (result.error || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error using template:', error)
        alert('Failed to use template: ' + (error.response?.data?.detail || error.message))
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
  background-color: rgba(255, 255, 255, 0.1);
}

.tabs-container {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #e5e5e5;
  padding: 0;
  background: white;
  margin: 0 2rem;
}

.tab-button {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  position: relative;
}

.tab-button:hover {
  color: #97144D;
}

.tab-button.active {
  color: #97144D;
  border-bottom-color: #97144D;
}

.templates-content {
  padding: 2rem;
  background: #f5f5f5;
  min-height: 400px;
  margin: 0;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.template-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s;
}

.template-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.template-card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.template-icon {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  background-color: #f3e8ff;
  color: #97144D;
  display: flex;
  align-items: center;
  justify-content: center;
}

.template-badge {
  font-size: 0.75rem;
}

.template-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.template-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.technologies-section {
  margin-bottom: 1rem;
}

.technologies-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-tag {
  padding: 0.25rem 0.75rem;
  background-color: #f3f4f6;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #374151;
  font-weight: 500;
}

.features-section {
  flex: 1;
  margin-bottom: 1rem;
}

.features-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.features-list li {
  font-size: 0.875rem;
  color: #6b7280;
  padding-left: 1.25rem;
  position: relative;
}

.features-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #97144D;
  font-weight: bold;
}

.use-template-button {
  background-color: #97144D;
  color: white;
  border: none;
  width: 100%;
  padding: 0.75rem;
  font-weight: 600;
  margin-top: auto;
}

.use-template-button:hover {
  background-color: #7a0f3d;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: white;
  border-top: 1px solid #e5e5e5;
}

.footer-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.close-footer-button {
  background-color: #97144D;
  color: white;
  border: none;
}

.close-footer-button:hover {
  background-color: #7a0f3d;
}

@media (max-width: 1024px) {
  .templates-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .templates-grid {
    grid-template-columns: 1fr;
  }
  
  .tabs-container {
    padding: 0 1rem;
    overflow-x: auto;
  }
  
  .tab-button {
    padding: 1rem;
    white-space: nowrap;
  }
  
  .templates-content {
    padding: 1rem;
  }
  
  .dialog-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }
}
</style>
