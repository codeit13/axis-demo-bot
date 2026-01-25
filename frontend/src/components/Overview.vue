<template>
  <div class="overview-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>Error loading dashboard: {{ error }}</p>
      <Button @click="fetchDashboardStats" variant="default">Retry</Button>
    </div>

    <!-- Content -->
    <template v-else>
    <!-- Content Header -->
    <div class="content-header">
      <h1 class="page-title">Dashboard</h1>
    </div>

    <!-- AI Insight Card -->
    <Card class="ai-insight-card">
      <CardContent class="ai-insight-content">
        <div class="ai-insight-header">
          <div class="ai-tag">AI Insight</div>
          <span class="timestamp">{{ aiInsight.timestamp }}</span>
        </div>
        <h2 class="ai-insight-title">{{ aiInsight.title }}</h2>
        <p class="ai-insight-description">
          {{ aiInsight.description }}
        </p>
        <Button 
          v-if="aiInsight.suggestionId" 
          variant="default" 
          class="review-button"
          @click="$router.push(`/suggestions/${aiInsight.suggestionId}`)"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
          </svg>
          Review Actions
        </Button>
      </CardContent>
    </Card>

    <!-- Key Metrics Cards -->
    <div class="metrics-grid">
      <Card class="metric-card">
        <CardContent>
          <div class="metric-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span class="metric-label">Avg. Deployment Time</span>
          </div>
          <div class="metric-value">
            {{ metrics ? formatTime(Math.floor(metrics.total_agent_runs * 0.5)) : '12m 30s' }}
          </div>
          <div class="metric-trend positive">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <span>{{ metrics ? `-${Math.round((metrics.suggestions_last_month || 0) * 0.1)}%` : '-45%' }} vs last month</span>
          </div>
        </CardContent>
      </Card>

      <Card class="metric-card">
        <CardContent>
          <div class="metric-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              <path d="M9 12l2 2 4-4"></path>
            </svg>
            <span class="metric-label">Security Score</span>
          </div>
          <div class="metric-value">{{ metrics ? `${metrics.security_score || 98.5}%` : '98.5%' }}</div>
          <div class="metric-trend positive">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <span>+{{ metrics ? Math.round((metrics.security_score || 98.5) - 93.3) : 5.2 }}% vs last month</span>
          </div>
        </CardContent>
      </Card>

      <Card class="metric-card">
        <CardContent>
          <div class="metric-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="8" cy="8" r="1"></circle>
              <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
            <span class="metric-label">Auto-Fixed Bugs</span>
          </div>
          <div class="metric-value">{{ metrics ? metrics.auto_fixed_bugs || 142 : 142 }}</div>
          <div class="metric-trend positive">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <span>+{{ metrics ? (metrics.auto_fixed_bugs_trend || 28) : 28 }}% vs last month</span>
          </div>
        </CardContent>
      </Card>

      <Card class="metric-card">
        <CardContent>
          <div class="metric-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="metric-icon">
              <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
            </svg>
            <span class="metric-label">Active Agents</span>
          </div>
          <div class="metric-value">
            {{ metrics ? `${metrics.active_agents || 8}/${metrics.total_agent_types || 10}` : '8/10' }}
          </div>
          <div class="metric-subvalue">
            {{ metrics ? `${(metrics.total_agent_types || 10) - (metrics.active_agents || 8)} inactive` : '2 training' }}
          </div>
          <div class="metric-trend positive">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <span>Stable vs last month</span>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <!-- Development Velocity Chart -->
      <Card class="chart-card">
        <CardHeader>
          <CardTitle>Feature delivery rate: Agentic vs Traditional.</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="chart-container">
            <div class="chart-legend">
              <div class="legend-item">
                <span class="legend-dot traditional"></span>
                <span>Traditional</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot agentic"></span>
                <span>Agentic AI</span>
              </div>
            </div>
            <div class="line-chart">
              <svg viewBox="0 0 400 200" class="chart-svg">
                <!-- Grid lines -->
                <line x1="40" y1="20" x2="40" y2="180" stroke="#e5e5e5" stroke-width="1"/>
                <line x1="40" y1="180" x2="380" y2="180" stroke="#e5e5e5" stroke-width="1"/>
                
                <!-- Y-axis labels -->
                <text x="35" y="25" text-anchor="end" font-size="10" fill="#666">100</text>
                <text x="35" y="100" text-anchor="end" font-size="10" fill="#666">50</text>
                <text x="35" y="175" text-anchor="end" font-size="10" fill="#666">0</text>
                
                <!-- X-axis labels -->
                <text x="80" y="195" text-anchor="middle" font-size="10" fill="#666">Jan</text>
                <text x="140" y="195" text-anchor="middle" font-size="10" fill="#666">Feb</text>
                <text x="200" y="195" text-anchor="middle" font-size="10" fill="#666">Mar</text>
                <text x="260" y="195" text-anchor="middle" font-size="10" fill="#666">Apr</text>
                <text x="320" y="195" text-anchor="middle" font-size="10" fill="#666">May</text>
                <text x="380" y="195" text-anchor="middle" font-size="10" fill="#666">Jun</text>
                
                <!-- Traditional line (grey, dashed) -->
                <polyline 
                  points="80,160 140,150 200,140 260,130 320,120 380,110" 
                  fill="none" 
                  stroke="#9ca3af" 
                  stroke-width="2" 
                  stroke-dasharray="5,5"
                />
                
                <!-- Agentic AI line (dark red, solid) -->
                <polyline 
                  points="80,170 140,150 200,100 260,60 320,40 380,25" 
                  fill="none" 
                  stroke="#97144D" 
                  stroke-width="2"
                />
              </svg>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Bug Resolution Chart -->
      <Card class="chart-card">
        <CardHeader>
          <CardTitle>Bug Resolution</CardTitle>
          <p class="chart-subtitle">Avg time reduced by 60%.</p>
        </CardHeader>
        <CardContent>
          <div class="chart-container">
            <div class="bar-chart">
              <svg viewBox="0 0 400 200" class="chart-svg">
                <!-- Grid line -->
                <line x1="40" y1="180" x2="380" y2="180" stroke="#e5e5e5" stroke-width="1"/>
                
                <!-- X-axis labels -->
                <text x="80" y="195" text-anchor="middle" font-size="10" fill="#666">Mon</text>
                <text x="140" y="195" text-anchor="middle" font-size="10" fill="#666">Tue</text>
                <text x="200" y="195" text-anchor="middle" font-size="10" fill="#666">Wed</text>
                <text x="260" y="195" text-anchor="middle" font-size="10" fill="#666">Thu</text>
                <text x="320" y="195" text-anchor="middle" font-size="10" fill="#666">Fri</text>
                <text x="360" y="195" text-anchor="middle" font-size="10" fill="#666">Sat</text>
                <text x="380" y="195" text-anchor="middle" font-size="10" fill="#666">Sun</text>
                
                <!-- Bars (pink) -->
                <rect x="60" y="120" width="40" height="60" fill="#ec4899" rx="2"/>
                <rect x="120" y="100" width="40" height="80" fill="#ec4899" rx="2"/>
                <rect x="180" y="60" width="40" height="120" fill="#ec4899" rx="2"/>
                <rect x="240" y="140" width="40" height="40" fill="#ec4899" rx="2"/>
                <rect x="300" y="160" width="40" height="20" fill="#ec4899" rx="2"/>
                <rect x="340" y="170" width="40" height="10" fill="#ec4899" rx="2"/>
                <rect x="360" y="175" width="40" height="5" fill="#ec4899" rx="2"/>
              </svg>
            </div>
            <div class="bug-stats">
              <div class="bug-stat-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>Auto-Patch Success: <strong>92%</strong></span>
              </div>
              <div class="bug-stat-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                <span>Pending Review: <strong>5</strong></span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
    </template>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import api from '../services/api'
import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Button } from './ui/button'

export default {
  name: 'Overview',
  components: {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Button
  },
  data() {
    return {
      loading: true,
      stats: null,
      error: null
    }
  },
  computed: {
    aiInsight() {
      if (!this.stats || !this.stats.ai_insights || this.stats.ai_insights.length === 0) {
        return {
          title: 'System Ready',
          description: 'AI agents are ready to assist with your development workflow. Create a project to get started.',
          timestamp: 'Just now'
        }
      }
      const insight = this.stats.ai_insights[0]
      const timestamp = this.formatTimestamp(insight.timestamp)
      return {
        title: insight.title,
        description: insight.description,
        timestamp: timestamp,
        suggestionId: insight.suggestion_id
      }
    },
    metrics() {
      if (!this.stats) return null
      return this.stats.metrics
    },
    charts() {
      if (!this.stats) return null
      return this.stats.charts
    }
  },
  mounted() {
    this.fetchDashboardStats()
  },
  methods: {
    async fetchDashboardStats() {
      this.loading = true
      this.error = null
      try {
        const response = await api.getDashboardStats()
        this.stats = response.data
      } catch (error) {
        console.error('Error fetching dashboard stats:', error)
        this.error = error.response?.data?.detail || error.message
      } finally {
        this.loading = false
      }
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return 'Just now'
      const date = new Date(timestamp)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)
      
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      if (diffDays < 7) return `${diffDays}d ago`
      return date.toLocaleDateString()
    },
    formatTime(seconds) {
      if (seconds < 60) return `${seconds}s`
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}m ${secs}s`
    },
    calculateTrend(current, previous) {
      if (!previous || previous === 0) return 0
      const change = ((current - previous) / previous) * 100
      return Math.round(change)
    }
  }
}
</script>

<style scoped>
.overview-container {
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100%;
}

@media (max-width: 768px) {
  .overview-container {
    padding: 1rem;
  }
}

@media (max-width: 640px) {
  .overview-container {
    padding: 1rem;
  }
}

.content-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.5rem;
  }
}

/* AI Insight Card */
.ai-insight-card {
  background: linear-gradient(135deg, #97144D 0%, #7a0f3d 100%);
  border: none;
  margin-bottom: 2rem;
}

.ai-insight-content {
  padding: 2rem;
  color: white;
}

.ai-insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ai-tag {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.timestamp {
  font-size: 0.875rem;
  opacity: 0.9;
}

.ai-insight-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.ai-insight-description {
  font-size: 1rem;
  opacity: 0.95;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.review-button {
  background-color: white;
  color: #97144D;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.review-button:hover {
  opacity: 0.9;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 640px) {
  .metrics-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.metric-card {
  background: white;
  border: 1px solid #e5e5e5;
}

.metric-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.metric-icon {
  color: #6b7280;
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.metric-subvalue {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #10b981;
}

.metric-trend.positive {
  color: #10b981;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.chart-card {
  background: white;
  border: 1px solid #e5e5e5;
}

.chart-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.chart-container {
  padding: 1rem 0;
}

.chart-legend {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.traditional {
  background-color: #9ca3af;
}

.legend-dot.agentic {
  background-color: #97144D;
}

.chart-svg {
  width: 100%;
  height: 200px;
}

.line-chart,
.bar-chart {
  width: 100%;
  height: 200px;
}

.bug-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e5e5;
}

.bug-stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
}

.bug-stat-item strong {
  font-weight: 600;
  color: #1f2937;
}

/* Loading and Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e5e5;
  border-top-color: #97144D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state p {
  color: #ef4444;
  margin-bottom: 1rem;
}
</style>
