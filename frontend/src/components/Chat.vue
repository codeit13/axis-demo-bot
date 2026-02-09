<template>
  <div class="chat-container">
    <div class="chat-header">
      <div class="header-content">
        <h1 class="chat-title">Chat</h1>
        <p class="chat-subtitle">Access centralized code repository, MCPs, and all agents</p>
      </div>
    </div>

    <div class="chat-main">
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-screen">
          <div class="welcome-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <h2 class="welcome-title">How can I help, Piyush?</h2>
          <p class="welcome-subtitle">Ask me anything about your codebase, Jira tickets, or use any agent</p>
          
          <div class="suggestions-section">
            <div class="suggestions-title">Try asking:</div>
            <div class="suggestions-grid">
              <Button 
                v-for="(suggestion, index) in suggestions" 
                :key="index"
                variant="outline"
                size="sm"
                class="suggestion-chip"
                @click="sendSuggestion(suggestion.text)"
              >
                {{ suggestion.text }}
              </Button>
            </div>
          </div>
        </div>

        <div v-for="(message, index) in messages" :key="index" class="message-wrapper" :class="message.role">
          <div class="message-content">
            <div v-if="message.role === 'user'" class="message-avatar user-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div v-else class="message-avatar assistant-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <line x1="9" y1="9" x2="15" y2="9"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
            </div>
            <div class="message-bubble" :class="message.role">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div v-if="message.agent" class="message-agent-badge">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
                {{ message.agent }}
              </div>
              <div v-else-if="message.agents && message.agents.length > 0" class="message-agent-badge">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
                {{ message.agents.join(', ') }}
              </div>
            </div>
          </div>
          <div class="message-actions" v-if="message.role === 'assistant'">
            <Button variant="ghost" size="sm" class="h-7 w-7 p-0" title="Copy">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </Button>
            <Button variant="ghost" size="sm" class="h-7 w-7 p-0" title="Like">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 10v12M17 10v12M3 10h18a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z"></path>
              </svg>
            </Button>
            <Button variant="ghost" size="sm" class="h-7 w-7 p-0" title="Dislike">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 14V2M7 14v12M21 14H3a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2z"></path>
              </svg>
            </Button>
          </div>
        </div>

        <div v-if="isLoading" class="message-wrapper assistant">
          <div class="message-content">
            <div class="message-avatar assistant-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <line x1="9" y1="9" x2="15" y2="9"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
            </div>
            <div class="message-bubble assistant">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-container" :class="{ 'has-agents': selectedAgents.length > 0 }">
        <div class="chat-input-wrapper">
          <div v-if="selectedAgents.length > 0" class="selected-agents-section">
            <div class="selected-agents-inline">
              <button
                v-for="agentId in selectedAgents" 
                :key="agentId"
                class="agent-badge-btn"
                @click.stop="removeAgent(agentId)"
                type="button"
              >
                <svg class="badge-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
                <span class="badge-text">{{ getAgentName(agentId) }}</span>
                <svg class="badge-remove-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="input-row">
            <div class="input-left-controls">
              <button 
                class="control-btn plus-btn"
                @click.stop="toggleAgentMenu"
                type="button"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
              <Teleport to="body">
                <div v-if="showAgentMenu" class="agent-menu-dropdown" :style="menuStyle" @click.stop>
                  <div 
                    v-for="agent in availableAgents.filter(a => !selectedAgents.includes(a.id))" 
                    :key="agent.id"
                    class="menu-item"
                    @click="addAgent(agent.id); showAgentMenu = false"
                  >
                    {{ agent.name }}
                  </div>
                  <div v-if="availableAgents.filter(a => !selectedAgents.includes(a.id)).length === 0" class="menu-item disabled">
                    No more agents available
                  </div>
                </div>
              </Teleport>
            </div>
            
            <Textarea
              v-model="inputText"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.shift.enter.exact="inputText += '\n'"
              placeholder="Ask anything..."
              class="chat-textarea"
              rows="1"
              ref="chatInput"
            />

            <div class="input-right-controls">
              <button class="control-btn mic-btn" type="button" title="Voice input">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                  <line x1="12" y1="19" x2="12" y2="23"></line>
                  <line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
              </button>
              <button 
                class="control-btn send-btn"
                @click="sendMessage"
                :disabled="!inputText.trim() || isLoading"
                type="button"
                title="Send message"
              >
                <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
                <div v-else class="spinner-small"></div>
              </button>
            </div>
          </div>
        </div>
        <div class="input-footer">
          <span class="footer-text">Chat can access code repository, Jira, and all agents</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Textarea } from './ui/textarea'
import { Button } from './ui/button'

export default {
  name: 'Chat',
  components: {
    Textarea,
    Button
  },
  data() {
    return {
      messages: [],
      inputText: '',
      isLoading: false,
      selectedAgents: [],
      showAgentMenu: false,
      menuClickHandled: false,
      menuStyle: {},
      availableAgents: [
        { id: 'code-generation', name: 'Code Generation Agent' },
        { id: 'security-guardian', name: 'Security Guardian Agent' },
        { id: 'integration', name: 'Integration Agent' },
        { id: 'knowledge', name: 'Knowledge Agent' },
        { id: 'code-template', name: 'Code Template Agent' },
        { id: 'prompt-amplifier', name: 'Prompt Amplifier Agent' },
        { id: 'test-data-ui', name: 'Test Data UI Agent' },
        { id: 'test-case-generator', name: 'Test Case Generator Agent' },
        { id: 'load-testing', name: 'Load Testing Agent' },
        { id: 'devops', name: 'DevOps Agent' },
        { id: 'documentation', name: 'Documentation Agent' }
      ],
      suggestions: [
        { text: 'Show me all microservices in the codebase' },
        { text: 'Find Jira tickets assigned to me' },
        { text: 'Generate a REST API template' },
        { text: 'Check security vulnerabilities in my code' },
        { text: 'Explain the authentication service architecture' },
        { text: 'Create integration code for payment gateway' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.autoResizeTextarea()
    })
    // Close menu when clicking outside
    this.closeMenuHandler = (e) => {
      // If menu click was just handled, skip this handler
      if (this.menuClickHandled) {
        return
      }
      
      // Use setTimeout to allow button click handlers to process first
      setTimeout(() => {
        if (!this.$el) return
        
        const plusButton = this.$el.querySelector('.plus-btn')
        const menu = this.$el.querySelector('.agent-menu-dropdown')
        
        // Don't close if clicking the plus button
        if (plusButton && (plusButton === e.target || plusButton.contains(e.target))) {
          return
        }
        
        // Don't close if clicking inside the menu
        if (menu && menu.contains(e.target)) {
          return
        }
        
        // Close if clicking outside
        if (!this.$el.contains(e.target)) {
          this.showAgentMenu = false
        }
      }, 50)
    }
    // Don't use capture phase - let button click process first
    document.addEventListener('click', this.closeMenuHandler)
  },
  beforeUnmount() {
    if (this.closeMenuHandler) {
      document.removeEventListener('click', this.closeMenuHandler)
    }
  },
  methods: {
    async sendMessage() {
      if (!this.inputText.trim() || this.isLoading) return

      const userMessage = {
        role: 'user',
        content: this.inputText.trim(),
        agents: this.selectedAgents.length > 0 
          ? this.selectedAgents.map(id => this.availableAgents.find(a => a.id === id)?.name).filter(Boolean)
          : null
      }

      this.messages.push(userMessage)
      const messageText = this.inputText.trim()
      this.inputText = ''
      this.isLoading = true

      // Call the backend API
      try {
        const api = (await import('../services/api.js')).default
        // For now, send the first selected agent or null
        const agentId = this.selectedAgents.length > 0 ? this.selectedAgents[0] : null
        const response = await api.sendChatMessage(messageText, agentId)
        
        this.messages.push({
          role: 'assistant',
          content: response.data.content || 'I apologize, but I encountered an error processing your request.',
          agent: response.data.agent
        })
      } catch (error) {
        console.error('Chat API error:', error)
        // Fallback to local response generation if API fails
        const response = this.generateResponse(messageText)
        this.messages.push({
          role: 'assistant',
          content: response.content || 'I apologize, but I encountered an error processing your request.',
          agent: response.agent
        })
      } finally {
        this.isLoading = false
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },

    sendSuggestion(text) {
      this.inputText = text
      this.$nextTick(() => {
        this.sendMessage()
      })
    },

    generateResponse(userInput) {
      const input = userInput.toLowerCase()
      let response = { content: '', agent: null }

      // Code repository queries
      if (this.matches(input, ['microservice', 'service', 'codebase', 'repository', 'code'])) {
        response.content = `I found **15 microservices** in the centralized code repository:\n\n` +
          `• **Authentication Service** (Python/FastAPI) - Handles JWT tokens and user management\n` +
          `• **Payment Gateway Service** (TypeScript/Node.js) - Processes payments via Stripe\n` +
          `• **Notification Service** (Go) - Sends emails and SMS\n` +
          `• **File Upload Service** (Java/Spring Boot) - Manages file storage on S3\n` +
          `• **Analytics Service** (Python/FastAPI) - Tracks user behavior\n\n` +
          `Would you like details about any specific service?`
        response.agent = 'Knowledge Agent'
      }
      // Jira queries
      else if (this.matches(input, ['jira', 'ticket', 'issue', 'bug', 'task', 'story'])) {
        response.content = `Here are your **Jira tickets**:\n\n` +
          `**Assigned to You (5 tickets):**\n` +
          `• [DEV-1234] Implement OAuth2 authentication - In Progress\n` +
          `• [DEV-1235] Fix payment gateway timeout issue - To Do\n` +
          `• [DEV-1236] Add rate limiting to API endpoints - In Review\n` +
          `• [DEV-1237] Update API documentation - To Do\n` +
          `• [DEV-1238] Performance optimization for user service - Backlog\n\n` +
          `**Recent Updates:**\n` +
          `• [DEV-1234] Code review completed, ready for testing\n` +
          `• [DEV-1236] PR merged, deploying to staging`
        response.agent = 'Jira MCP'
      }
      // Code generation/template queries
      else if (this.matches(input, ['generate', 'create', 'template', 'boilerplate', 'scaffold'])) {
        response.content = `I can help you generate code! Here are available templates:\n\n` +
          `**REST API Microservice** - Complete FastAPI service with PostgreSQL\n` +
          `**gRPC Microservice** - Protocol buffers and service definitions\n` +
          `**Event-Driven Service** - RabbitMQ integration with event handlers\n` +
          `**GraphQL API** - Schema definitions and resolvers\n\n` +
          `Which template would you like? I can also create custom code based on your requirements.`
        response.agent = 'Code Template Agent'
      }
      // Security queries
      else if (this.matches(input, ['security', 'vulnerability', 'vulnerable', 'secure', 'owasp', 'encryption'])) {
        response.content = `**Security Analysis Results:**\n\n` +
          `✅ **No critical vulnerabilities found**\n\n` +
          `**Recommendations:**\n` +
          `• All API endpoints use HTTPS\n` +
          `• JWT tokens properly signed and validated\n` +
          `• SQL injection protection in place\n` +
          `• Rate limiting enabled on all endpoints\n\n` +
          `**Minor Issues:**\n` +
          `• Consider adding Content Security Policy headers\n` +
          `• Update dependency: axios@0.21.1 → 0.28.0 (security patch available)`
        response.agent = 'Security Guardian Agent'
      }
      // Architecture/explanation queries
      else if (this.matches(input, ['explain', 'architecture', 'how', 'works', 'structure', 'design'])) {
        response.content = `**Authentication Service Architecture:**\n\n` +
          `**Components:**\n` +
          `• **API Layer** - FastAPI routes handling login, register, refresh token\n` +
          `• **Service Layer** - Business logic for password hashing, token generation\n` +
          `• **Database** - PostgreSQL storing user credentials and sessions\n` +
          `• **Redis** - Token blacklist for logout functionality\n\n` +
          `**Flow:**\n` +
          `1. User submits credentials → API validates\n` +
          `2. Service hashes password and checks against DB\n` +
          `3. On success, generates JWT access + refresh tokens\n` +
          `4. Tokens stored in Redis for session management\n` +
          `5. Subsequent requests validated via JWT middleware`
        response.agent = 'Knowledge Agent'
      }
      // Integration queries
      else if (this.matches(input, ['integration', 'integrate', 'api', 'connect', 'endpoint'])) {
        response.content = `**Integration Code Generated:**\n\n` +
          `\`\`\`typescript\n` +
          `// Payment Gateway Integration\n` +
          `import { PaymentService } from '@axis-bank/payment-sdk';\n\n` +
          `const paymentService = new PaymentService({\n` +
          `  apiKey: process.env.PAYMENT_API_KEY,\n` +
          `  environment: 'production'\n` +
          `});\n\n` +
          `async function processPayment(amount, currency) {\n` +
          `  return await paymentService.charge({\n` +
          `    amount,\n` +
          `    currency,\n` +
          `    description: 'Payment processing'\n` +
          `  });\n` +
          `}\n` +
          `\`\`\`\n\n` +
          `I've also generated:\n` +
          `• API contract documentation\n` +
          `• Error handling examples\n` +
          `• Unit tests\n` +
          `• Integration test scenarios`
        response.agent = 'Integration Agent'
      }
      // Default response
      else {
        response.content = `I understand you're asking about "${userInput}". Let me help you with that.\n\n` +
          `I have access to:\n` +
          `• **Centralized Code Repository** - All microservices and codebase\n` +
          `• **Jira MCP** - Project management and tickets\n` +
          `• **All AI Agents** - Code generation, security, integration, and more\n\n` +
          `Could you be more specific? For example:\n` +
          `• "Show me the authentication service code"\n` +
          `• "Find my open Jira tickets"\n` +
          `• "Generate a REST API template"\n` +
          `• "Check for security issues"`
        response.agent = null
      }

      // Enhance response with API call simulation
      return this.enhanceResponse(response, userInput)
    },

    matches(input, keywords) {
      return keywords.some(keyword => input.includes(keyword))
    },

    async enhanceResponse(response, userInput) {
      // Simulate API call to improve response
      try {
        // Mock API call - in real implementation, this would call an actual API
        const enhanced = await this.mockEnhanceAPI(response.content, userInput)
        return {
          content: enhanced,
          agent: response.agent
        }
      } catch (error) {
        return response
      }
    },

    mockEnhanceAPI(content, userInput) {
      // Simulate API processing delay
      return new Promise((resolve) => {
        setTimeout(() => {
          // Add some refinement to make it feel more AI-generated
          let enhanced = content
          
          // Add contextual improvements
          if (userInput.includes('?')) {
            enhanced = enhanced.replace(/\n\n/g, '\n\n💡 ')
          }
          
          // Add emoji for better UX
          if (enhanced.includes('**')) {
            enhanced = enhanced.replace(/\*\*([^*]+)\*\*/g, '**$1**')
          }
          
          resolve(enhanced)
        }, 300)
      })
    },

    formatMessage(text) {
      // Handle undefined/null values
      if (!text) return ''
      
      // Convert markdown-like formatting to HTML
      return String(text)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/```([\s\S]+?)```/g, '<pre><code>$1</code></pre>')
        .replace(/\n/g, '<br>')
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },

    addAgent(agentId) {
      if (agentId && !this.selectedAgents.includes(agentId)) {
        this.selectedAgents.push(agentId)
      }
    },

    removeAgent(agentId) {
      this.selectedAgents = this.selectedAgents.filter(id => id !== agentId)
    },

    getAgentName(agentId) {
      const agent = this.availableAgents.find(a => a.id === agentId)
      return agent ? agent.name : agentId
    },

    toggleAgentMenu(e) {
      if (e) {
        e.stopPropagation()
        e.preventDefault()
      }
      this.menuClickHandled = true
      this.showAgentMenu = !this.showAgentMenu
      
      if (this.showAgentMenu) {
        this.$nextTick(() => {
          this.updateMenuPosition()
        })
      }
      
      // Reset flag after a short delay
      setTimeout(() => {
        this.menuClickHandled = false
      }, 100)
    },

    updateMenuPosition() {
      const plusButton = this.$el?.querySelector('.plus-btn')
      if (plusButton) {
        const rect = plusButton.getBoundingClientRect()
        this.menuStyle = {
          position: 'fixed',
          top: `${rect.top - 8}px`,
          left: `${rect.left}px`,
          transform: 'translateY(-100%)',
          zIndex: 10000
        }
      }
    },

    autoResizeTextarea() {
      // Set up initial resize
      this.$nextTick(() => {
        this.resizeTextarea()
      })
    },
    
    resizeTextarea() {
      const textareaRef = this.$refs.chatInput
      if (!textareaRef) return
      
      // For Vue 3 components with script setup, access the DOM element
      let textarea = null
      
      // Try different ways to access the textarea element
      if (textareaRef.$el) {
        // Component instance with $el
        textarea = textareaRef.$el.tagName === 'TEXTAREA' ? textareaRef.$el : textareaRef.$el.querySelector?.('textarea')
      } else if (textareaRef instanceof HTMLElement) {
        // Already a DOM element
        textarea = textareaRef
      } else if (textareaRef.getElementsByTagName) {
        // Try getElementsByTagName if available
        const elements = textareaRef.getElementsByTagName('textarea')
        textarea = elements?.[0]
      }
      
      // If still not found, try querySelector on the input container
      if (!textarea) {
        const container = this.$el?.querySelector?.('.chat-input-container')
        if (container) {
          textarea = container.querySelector('textarea')
        }
      }
      
      if (textarea && textarea.tagName === 'TEXTAREA') {
        textarea.style.height = 'auto'
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
      }
    }
  },
  watch: {
    messages() {
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
    inputText() {
      this.$nextTick(() => {
        this.resizeTextarea()
      })
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 73px);
  background: white;
}

.chat-header {
  border-bottom: 1px solid #e5e5e5;
  padding: 1.5rem 2rem;
  background: white;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.chat-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.chat-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background: white;
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.welcome-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #97144D 0%, #7a0f3d 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.welcome-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 2rem;
}

.suggestions-section {
  width: 100%;
  max-width: 800px;
}

.suggestions-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.suggestions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.suggestion-chip {
  white-space: nowrap;
}

.message-wrapper {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}

.message-wrapper.user {
  align-items: flex-end;
}

.message-wrapper.assistant {
  align-items: flex-start;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  max-width: 80%;
}

.message-wrapper.user .message-content {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar {
  background: #97144D;
  color: white;
}

.assistant-avatar {
  background: #e5e5e5;
  color: #6b7280;
}

.message-bubble {
  padding: 0.875rem 1.125rem;
  border-radius: 12px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message-bubble.user {
  background: #97144D;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-bubble.assistant {
  background: white;
  color: #1f2937;
  border: 1px solid #e5e5e5;
  border-bottom-left-radius: 4px;
}

.message-text {
  font-size: 0.9375rem;
}

.message-text :deep(strong) {
  font-weight: 600;
}

.message-text :deep(code) {
  background: #f3f4f6;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-size: 0.875em;
  font-family: 'Monaco', 'Courier New', monospace;
}

.message-text :deep(pre) {
  background: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.message-text :deep(pre code) {
  background: transparent;
  color: inherit;
  padding: 0;
}

.message-agent-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
  padding-top: 0.5rem;
  border-top: 1px solid #e5e5e5;
}

.message-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  margin-left: 44px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 0.5rem 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #9ca3af;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.chat-input-container {
  border-top: 1px solid #e5e5e5;
  background: white;
  padding: 1rem 2rem;
}

.chat-input-container.has-agents {
  padding: 1.5rem 2rem;
}

.chat-input-wrapper {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 24px;
  padding: 0.5rem 0.75rem;
  transition: all 0.2s;
  min-height: 48px;
}

.chat-input-wrapper.has-agents {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.selected-agents-section {
  width: 100%;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 0.5rem;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.chat-input-wrapper:focus-within {
  border-color: #e5e5e5;
  box-shadow: none;
}

.input-left-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  flex-shrink: 0;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  padding: 0.375rem;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.875rem;
  gap: 0.375rem;
}

.control-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.plus-btn {
  color: #1f2937;
}

.think-btn {
  color: #3b82f6;
  font-weight: 500;
}

.think-btn:hover {
  background: #eff6ff;
  color: #2563eb;
}

.mic-btn {
  color: #6b7280;
}

.send-btn {
  background: #1f2937;
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  padding: 0;
}

.send-btn:hover:not(:disabled) {
  background: #111827;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
}

.chat-textarea {
  flex: 1;
  min-height: 40px;
  min-width: 200px;
  max-height: 120px;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  font-size: 0.9375rem;
  font-family: inherit;
  resize: none;
  overflow-y: auto;
  color: #1f2937;
  outline: none;
  box-shadow: none;
}

.chat-textarea:focus {
  outline: none;
  box-shadow: none;
  border: none;
}

.chat-textarea:focus-visible {
  outline: none;
  box-shadow: none;
}

.chat-textarea::placeholder {
  color: #9ca3af;
}

.input-right-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.selected-agents-inline {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  flex-wrap: wrap;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
  width: 100%;
}

.selected-agents-inline::-webkit-scrollbar {
  display: none;
}

.agent-badge-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  border: none;
  background: transparent;
  color: #3b82f6;
  cursor: pointer;
  padding: 0.375rem 0.625rem;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
  position: relative;
}

.agent-badge-btn:hover {
  background: #eff6ff;
  color: #2563eb;
}

.agent-badge-btn .badge-icon {
  flex-shrink: 0;
  opacity: 0.8;
}

.agent-badge-btn .badge-text {
  white-space: nowrap;
}

.agent-badge-btn .badge-remove-icon {
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.2s ease;
  margin-left: 0.25rem;
  flex-shrink: 0;
}

.agent-badge-btn:hover .badge-remove-icon {
  opacity: 1;
  transform: scale(1);
}

.agent-menu-dropdown {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  min-width: 200px;
  max-width: 300px;
  max-height: 300px;
  overflow-y: auto;
  display: block;
}

.menu-item {
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background: #f3f4f6;
}

.menu-item.disabled {
  color: #9ca3af;
  cursor: not-allowed;
}


.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.input-footer {
  margin-top: 0.5rem;
  text-align: center;
}

.footer-text {
  font-size: 0.75rem;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .message-content {
    max-width: 90%;
  }
  
  .chat-input-container {
    padding: 1rem;
  }
}
</style>
