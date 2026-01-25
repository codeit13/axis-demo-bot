import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    issues: [],
    currentIssue: null,
    filterProjectId: null,
    loading: false,
    error: null
  },
  mutations: {
    SET_ISSUES(state, issues) {
      state.issues = issues
    },
    SET_CURRENT_ISSUE(state, issue) {
      state.currentIssue = issue
    },
    ADD_ISSUE(state, issue) {
      state.issues.push(issue)
    },
    UPDATE_ISSUE(state, issue) {
      const index = state.issues.findIndex(i => i.id === issue.id)
      if (index !== -1) {
        state.issues.splice(index, 1, issue)
      }
    },
    SET_FILTER_PROJECT_ID(state, projectId) {
      state.filterProjectId = projectId
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    async fetchIssues({ commit, state, rootState }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        if (state.filterProjectId) {
          const response = await api.getIssues(state.filterProjectId)
          commit('SET_ISSUES', response.data)
          return response.data
        } else {
          // Fetch from all projects
          const projects = rootState.projects.projects || []
          const allIssues = []
          for (const project of projects) {
            try {
              const response = await api.getIssues(project.id)
              allIssues.push(...response.data)
            } catch (error) {
              console.error(`Failed to fetch issues for project ${project.id}:`, error)
            }
          }
          commit('SET_ISSUES', allIssues)
          return allIssues
        }
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchIssuesByProject({ commit }, projectId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.getIssues(projectId)
        commit('SET_ISSUES', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createIssue({ commit, dispatch }, { projectId, issueData }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.createIssue(projectId, issueData)
        commit('ADD_ISSUE', response.data)
        await dispatch('fetchIssuesByProject', projectId)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async updateIssueStatus({ commit, dispatch }, { issueId, status }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.updateIssueStatus(issueId, status)
        commit('UPDATE_ISSUE', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    setFilterProjectId({ commit, dispatch }, projectId) {
      commit('SET_FILTER_PROJECT_ID', projectId)
      if (projectId) {
        dispatch('fetchIssuesByProject', projectId)
      } else {
        dispatch('fetchIssues')
      }
    }
  },
  getters: {
    getIssueById: (state) => (id) => {
      return state.issues.find(i => i.id === id)
    }
  }
}
