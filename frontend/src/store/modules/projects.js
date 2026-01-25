import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    projects: [],
    currentProject: null,
    codeFiles: {},
    loading: false,
    error: null
  },
  mutations: {
    SET_PROJECTS(state, projects) {
      state.projects = projects
    },
    SET_CURRENT_PROJECT(state, project) {
      state.currentProject = project
    },
    SET_CODE_FILES(state, { projectId, files }) {
      state.codeFiles = { ...state.codeFiles, [projectId]: files }
    },
    ADD_CODE_FILE(state, { projectId, file }) {
      const files = state.codeFiles[projectId] || []
      state.codeFiles = {
        ...state.codeFiles,
        [projectId]: [...files, file]
      }
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    async fetchProjects({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.getProjects()
        commit('SET_PROJECTS', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchProject({ commit }, projectId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.getProject(projectId)
        commit('SET_CURRENT_PROJECT', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createProject({ commit, dispatch }, projectData) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.createProject(projectData)
        await dispatch('fetchProjects')
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchCodeFiles({ commit }, projectId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.getCodeFiles(projectId)
        commit('SET_CODE_FILES', { projectId, files: response.data })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createCodeFile({ commit, dispatch }, { projectId, fileData }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.createCodeFile(projectId, fileData)
        commit('ADD_CODE_FILE', { projectId, file: response.data })
        await dispatch('fetchCodeFiles', projectId)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  getters: {
    getProjectById: (state) => (id) => {
      return state.projects.find(p => p.id === id)
    },
    getCodeFilesByProjectId: (state) => (projectId) => {
      return state.codeFiles[projectId] || []
    }
  }
}
