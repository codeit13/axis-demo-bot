<template>
  <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-6xl max-h-[90vh] border-0 flex flex-col p-0">
      <!-- Header - Fixed -->
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

      <!-- Scrollable Content -->
      <div class="dialog-body">
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
                <div class="template-header-right">
                  <div class="template-stats">
                    <div 
                      class="template-stat-item stat-hoverable" 
                      @mouseenter="showTooltip($event, template.id, 'users')"
                      @mouseleave="hideTooltip('users')"
                    >
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="stat-icon">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                      <span class="stat-value">{{ getTemplateStats(template.id).users }}</span>
                    </div>
                    <div 
                      class="template-stat-item stat-hoverable"
                      @mouseenter="showTooltip($event, template.id, 'creator')"
                      @mouseleave="hideTooltip('creator')"
                    >
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="stat-icon">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                      </svg>
                      <span class="stat-value" :title="getTemplateStats(template.id).creator">
                        {{ getTemplateStats(template.id).creator }}
                      </span>
                    </div>
                  </div>
                  <Badge :variant="getBadgeVariant(template.type)" class="template-badge">
                    {{ template.type }}
                  </Badge>
                </div>
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

      </div>
    </DialogContent>
    <!-- Tooltip Portal - Outside dialog to avoid z-index issues -->
    <Teleport to="body">
      <div 
        v-if="activeTooltip" 
        class="stat-tooltip-portal"
        :style="tooltipStyle"
      >
        <div class="tooltip-content">
          <div class="tooltip-title" v-if="activeTooltip.type === 'users'">Usage Analytics</div>
          <div class="tooltip-title" v-else>Template Info</div>
          <template v-if="activeTooltip.type === 'users'">
            <div class="tooltip-row">
              <span class="tooltip-label">Users:</span>
              <span class="tooltip-number">{{ getTemplateStats(activeTooltip.templateId).users }}</span>
            </div>
            <div class="tooltip-row">
              <span class="tooltip-label">Times Used:</span>
              <span class="tooltip-number">{{ getTemplateStats(activeTooltip.templateId).timesUsed }}</span>
            </div>
          </template>
          <template v-else>
            <div class="tooltip-row">
              <span class="tooltip-label">Created by:</span>
              <span class="tooltip-text">{{ getTemplateStats(activeTooltip.templateId).creator }}</span>
            </div>
            <div class="tooltip-row">
              <span class="tooltip-label">Team:</span>
              <span class="tooltip-text">{{ getTemplateStats(activeTooltip.templateId).team }}</span>
            </div>
            <div class="tooltip-members" v-if="getTemplateStats(activeTooltip.templateId).teamMembers && getTemplateStats(activeTooltip.templateId).teamMembers.length > 0">
              <div class="tooltip-label">Members:</div>
              <div class="tooltip-member-list">
                <div class="tooltip-member-item" v-for="(member, index) in getTemplateStats(activeTooltip.templateId).teamMembers" :key="index">
                  <div class="member-avatar" :style="{ backgroundColor: getMemberColor(member) }">
                    {{ getMemberInitials(member) }}
                  </div>
                  <span class="member-name">{{ member }}</span>
                </div>
              </div>
            </div>
            <div class="tooltip-desc">Responsible for development & maintenance</div>
          </template>
        </div>
      </div>
    </Teleport>
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
      activeTooltip: null,
      tooltipStyle: {},
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
      ],
      templateStats: {
        1: { users: 45, timesUsed: 312, creator: 'Rajesh Kumar', team: 'Platform Team', teamMembers: ['Rajesh Kumar', 'Priya Sharma', 'Amit Mishra'], contributors: '3 members' },
        2: { users: 67, timesUsed: 489, creator: 'Priya Sharma', team: 'Backend Team', teamMembers: ['Priya Sharma', 'Vikram Tiwari', 'Kavita Nair', 'Rohit Desai', 'Suresh Kapoor'], contributors: '5 members' },
        3: { users: 28, timesUsed: 156, creator: 'Amit Mishra', team: 'Integration Team', teamMembers: ['Amit Mishra', 'Anjali Patel'], contributors: '2 members' },
        4: { users: 34, timesUsed: 201, creator: 'Sneha Reddy', team: 'Frontend Team', teamMembers: ['Sneha Reddy', 'Arjun Singh', 'Meera Verma', 'Nikhil Pandey'], contributors: '4 members' },
        5: { users: 52, timesUsed: 378, creator: 'Vikram Tiwari', team: 'Platform Team', teamMembers: ['Vikram Tiwari', 'Rajesh Kumar', 'Priya Sharma'], contributors: '3 members' },
        6: { users: 41, timesUsed: 267, creator: 'Anjali Patel', team: 'Payment Team', teamMembers: ['Anjali Patel', 'Ravi Mehta'], contributors: '2 members' }
      }
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
          // Merge with existing stats if available
          this.templates.forEach(template => {
            if (!this.templateStats[template.id]) {
              this.templateStats[template.id] = {
                users: Math.floor(Math.random() * 50) + 20,
                timesUsed: Math.floor(Math.random() * 400) + 100,
                creator: 'Team Member',
                team: 'Platform Team',
                teamMembers: ['Rajesh Kumar', 'Priya Sharma'],
                contributors: '2-4 members'
              }
            }
          })
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
    getTemplateStats(templateId) {
      return this.templateStats[templateId] || { 
        users: 0, 
        timesUsed: 0, 
        creator: 'N/A', 
        team: 'N/A',
        teamMembers: [],
        contributors: ''
      }
    },
    getMemberInitials(name) {
      if (!name) return '?'
      const parts = name.split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    },
    getMemberColor(name) {
      // Generate a consistent color based on the name
      const colors = [
        '#97144D', '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
        '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16', '#f97316'
      ]
      let hash = 0
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
      }
      return colors[Math.abs(hash) % colors.length]
    },
    truncateName(name) {
      if (!name) return 'N/A'
      const parts = name.split(' ')
      if (parts.length > 1) {
        // For Indian names, show first name and last name initial
        return parts[0] + ' ' + parts[parts.length - 1].charAt(0) + '.'
      }
      return name.length > 12 ? name.substring(0, 12) + '...' : name
    },
    showTooltip(event, templateId, type) {
      const rect = event.currentTarget.getBoundingClientRect()
      this.activeTooltip = { templateId, type }
      this.$nextTick(() => {
        // Calculate position - tooltip appears just above the stat item
        const right = window.innerWidth - rect.right
        
        this.tooltipStyle = {
          position: 'fixed',
          top: `${rect.top - 8}px`, // 8px gap above the icon
          right: `${right}px`,
          zIndex: 10002,
          transform: 'translateY(-100%)' // Move up by its own height
        }
      })
    },
    hideTooltip() {
      this.activeTooltip = null
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

.dialog-body {
  overflow-y: auto;
  overflow-x: visible;
  flex: 1;
  padding: 0;
  position: relative;
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

.dialog-body {
  padding: 0;
}

.tabs-container {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #e5e5e5;
  padding: 0;
  background: white;
  margin: 0;
  position: sticky;
  top: 0;
  z-index: 5;
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
  position: relative;
  overflow: visible;
}

.dialog-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e5e5;
  background: white;
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
  position: relative;
  z-index: 1;
  isolation: isolate;
}

.template-card:hover {
  z-index: 2;
}

.template-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.template-card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.template-header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex-shrink: 0;
}

.template-stats {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.template-stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  position: relative;
  z-index: 10;
}

.stat-hoverable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-hoverable:hover {
  transform: translateY(-1px);
}

.stat-hoverable:hover .stat-icon {
  color: #97144D;
}

.stat-hoverable:hover .stat-value {
  color: #97144D;
}

.stat-icon {
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.stat-value {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #6b7280;
  white-space: nowrap;
  transition: color 0.2s ease;
}

/* Stat Tooltip Portal */
.stat-tooltip-portal {
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.tooltip-content {
  background: #1f2937;
  color: white;
  padding: 0.625rem 0.875rem;
  border-radius: 8px;
  font-size: 0.75rem;
  min-width: 160px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  position: relative;
  white-space: nowrap;
}

.tooltip-content::after {
  content: '';
  position: absolute;
  top: 100%;
  right: 1rem;
  transform: translateX(0);
  border: 5px solid transparent;
  border-top-color: #1f2937;
}

.tooltip-title {
  font-size: 0.625rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  font-weight: 600;
  white-space: nowrap;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.375rem;
  gap: 0.5rem;
}

.tooltip-row:last-child {
  margin-bottom: 0;
}

.tooltip-label {
  font-size: 0.75rem;
  color: #d1d5db;
  white-space: nowrap;
}

.tooltip-number {
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
  white-space: nowrap;
}

.tooltip-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-align: right;
  white-space: nowrap;
}

.tooltip-desc {
  font-size: 0.625rem;
  color: #d1d5db;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  white-space: nowrap;
}

.tooltip-members {
  margin-top: 0.5rem;
}

.tooltip-member-list {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-top: 0.375rem;
}

.tooltip-member-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.member-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.member-name {
  font-size: 0.75rem;
  color: white;
  white-space: nowrap;
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
