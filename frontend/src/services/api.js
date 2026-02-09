import axios from 'axios'

// Determine base URL based on MODE environment variable
// Vite exposes env variables prefixed with VITE_
const getBaseURL = () => {
  // Get MODE from Vite env (exposed via vite.config.js)
  const mode = import.meta.env.VITE_MODE || 'DEV'
  
  if (mode === 'PROD' || mode === 'production') {
    // In production, use the current hostname
    const protocol = window.location.protocol
    const hostname = window.location.hostname
    const port = window.location.port ? `:${window.location.port}` : ''
    return `${protocol}//${hostname}${port}/api`
  } else {
    // In development, use localhost
    return 'http://localhost:8000/api'
  }
}

const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Projects
  getProjects() {
    return api.get('/projects/')
  },
  getProject(id) {
    return api.get(`/projects/${id}`)
  },
  createProject(project) {
    return api.post('/projects/', project)
  },
  getCodeFiles(projectId) {
    return api.get(`/projects/${projectId}/files`)
  },
  createCodeFile(projectId, file) {
    return api.post(`/projects/${projectId}/files`, file)
  },
  getCodeFile(projectId, fileId) {
    return api.get(`/projects/${projectId}/files/${fileId}`)
  },

  // Agents
  getAgentTypes() {
    return api.get('/agents/types')
  },
  runAgent(agentType, request) {
    return api.post(`/agents/${agentType}/analyze`, request)
  },

  // Suggestions
  getSuggestions(params = {}) {
    return api.get('/suggestions/', { params })
  },
  getSuggestion(id) {
    return api.get(`/suggestions/${id}`)
  },

  // Approvals
  approveSuggestion(suggestionId, action, comments = '') {
    return api.post(`/approvals/suggestions/${suggestionId}/approve`, {
      user_action: action,
      comments
    })
  },
  getApprovalHistory(suggestionId) {
    return api.get(`/approvals/suggestions/${suggestionId}/history`)
  },

  // Issues
  createIssue(projectId, issue) {
    return api.post(`/issues/projects/${projectId}/issues`, issue)
  },
  getIssues(projectId) {
    return api.get(`/issues/projects/${projectId}/issues`)
  },
  getIssue(issueId) {
    return api.get(`/issues/${issueId}`)
  },
  updateIssueStatus(issueId, status) {
    return api.patch(`/issues/${issueId}/status?status=${status}`)
  },

  // Business Rules
  getBusinessRules(projectId, status) {
    const params = status ? { status } : {}
    return api.get(`/business-rules/projects/${projectId}/rules`, { params })
  },
  createBusinessRule(projectId, rule) {
    return api.post(`/business-rules/projects/${projectId}/rules`, rule)
  },
  getBusinessRule(ruleId) {
    return api.get(`/business-rules/rules/${ruleId}`)
  },
  updateBusinessRule(ruleId, rule) {
    return api.put(`/business-rules/rules/${ruleId}`, rule)
  },
  approveBusinessRule(ruleId, approvedBy) {
    return api.post(`/business-rules/rules/${ruleId}/approve`, { approved_by: approvedBy })
  },
  getRuleVersions(ruleId) {
    return api.get(`/business-rules/rules/${ruleId}/versions`)
  },

  // Change Impact
  analyzeChangeImpact(request) {
    return api.post('/change-impact/analyze', request)
  },
  getChangeImpacts(projectId) {
    return api.get(`/change-impact/projects/${projectId}/impacts`)
  },
  getChangeImpact(impactId) {
    return api.get(`/change-impact/${impactId}`)
  },

  // Orchestration
  runAgentSequence(request) {
    return api.post('/orchestration/run-sequence', request)
  },
  triggerByChange(projectId, changeType, ruleIds) {
    return api.post('/orchestration/trigger-by-change', {
      project_id: projectId,
      change_type: changeType,
      rule_ids: ruleIds
    })
  },

  // Dashboard
  getDashboardStats() {
    return api.get('/dashboard/stats')
  },

  // Chat
  sendChatMessage(message, agentId = null) {
    return api.post('/chat/message', {
      message,
      agent_id: agentId
    })
  }
}
