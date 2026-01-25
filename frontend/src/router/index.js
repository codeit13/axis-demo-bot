import { createRouter, createWebHistory } from 'vue-router'
import Overview from '../components/Overview.vue'
import Dashboard from '../components/Dashboard.vue'
import ProjectDetail from '../components/ProjectDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Overview',
    component: Overview
  },
  {
    path: '/agent-hub',
    name: 'AgentHub',
    component: Dashboard
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: ProjectDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
