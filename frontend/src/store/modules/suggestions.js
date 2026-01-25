import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    suggestions: [],
    currentSuggestion: null,
    filters: {
      agent_type: '',
      status: ''
    },
    loading: false,
    error: null
  },
  mutations: {
    SET_SUGGESTIONS(state, suggestions) {
      state.suggestions = suggestions
    },
    SET_CURRENT_SUGGESTION(state, suggestion) {
      state.currentSuggestion = suggestion
    },
    SET_FILTERS(state, filters) {
      state.filters = { ...state.filters, ...filters }
    },
    UPDATE_SUGGESTION(state, suggestion) {
      const index = state.suggestions.findIndex(s => s.id === suggestion.id)
      if (index !== -1) {
        state.suggestions.splice(index, 1, suggestion)
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
    async fetchSuggestions({ commit, state }, params = {}) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const requestParams = { ...params }
        if (state.filters.agent_type) requestParams.agent_type = state.filters.agent_type
        if (state.filters.status) requestParams.status = state.filters.status
        
        const response = await api.getSuggestions(requestParams)
        commit('SET_SUGGESTIONS', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchSuggestion({ commit }, suggestionId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.getSuggestion(suggestionId)
        commit('SET_CURRENT_SUGGESTION', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async approveSuggestion({ commit, dispatch }, { suggestionId, action, comments = '' }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        await api.approveSuggestion(suggestionId, action, comments)
        await dispatch('fetchSuggestions')
        return true
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    setFilters({ commit, dispatch }, filters) {
      commit('SET_FILTERS', filters)
      dispatch('fetchSuggestions')
    }
  },
  getters: {
    filteredSuggestions: (state) => {
      let filtered = state.suggestions
      if (state.filters.agent_type) {
        filtered = filtered.filter(s => s.agent_type === state.filters.agent_type)
      }
      if (state.filters.status) {
        filtered = filtered.filter(s => s.status === state.filters.status)
      }
      return filtered
    }
  }
}
