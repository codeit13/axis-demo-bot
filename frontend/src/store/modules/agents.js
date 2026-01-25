import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    agentTypes: [],
    loading: {},
    lastResult: null,
    error: null
  },
  mutations: {
    SET_AGENT_TYPES(state, types) {
      state.agentTypes = types
    },
    SET_LOADING(state, { agentType, loading }) {
      state.loading = { ...state.loading, [agentType]: loading }
    },
    SET_LAST_RESULT(state, result) {
      state.lastResult = result
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    async fetchAgentTypes({ commit }) {
      try {
        const response = await api.getAgentTypes()
        // Sort: production agents first
        const productionAgents = [
          'business_logic_policy',
          'product_requirements',
          'api_contract',
          'technical_architecture',
          'quality_test',
          'change_impact',
          'release_readiness'
        ]
        const sorted = response.data.agent_types.sort((a, b) => {
          const aIsProd = productionAgents.includes(a.value)
          const bIsProd = productionAgents.includes(b.value)
          if (aIsProd && !bIsProd) return -1
          if (!aIsProd && bIsProd) return 1
          return 0
        })
        commit('SET_AGENT_TYPES', sorted)
        return sorted
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message)
        throw error
      }
    },
    async runAgent({ commit }, { agentType, request }) {
      commit('SET_LOADING', { agentType, loading: true })
      commit('SET_ERROR', null)
      try {
        const response = await api.runAgent(agentType, request)
        commit('SET_LAST_RESULT', response.data)
        return response.data
      } catch (error) {
        const errorMsg = error.response?.data?.detail || error.message
        commit('SET_ERROR', errorMsg)
        commit('SET_LAST_RESULT', { status: 'error', error: errorMsg })
        throw error
      } finally {
        commit('SET_LOADING', { agentType, loading: false })
      }
    },
    async runAgentSequence({ commit }, request) {
      commit('SET_LOADING', { sequence: true })
      commit('SET_ERROR', null)
      try {
        const response = await api.runAgentSequence(request)
        return response.data
      } catch (error) {
        const errorMsg = error.response?.data?.detail || error.message
        commit('SET_ERROR', errorMsg)
        throw error
      } finally {
        commit('SET_LOADING', { sequence: false })
      }
    },
    async triggerByChange({ commit }, { projectId, changeType, ruleIds }) {
      commit('SET_LOADING', { changeImpact: true })
      commit('SET_ERROR', null)
      try {
        const response = await api.triggerByChange(projectId, changeType, ruleIds)
        return response.data
      } catch (error) {
        const errorMsg = error.response?.data?.detail || error.message
        commit('SET_ERROR', errorMsg)
        throw error
      } finally {
        commit('SET_LOADING', { changeImpact: false })
      }
    }
  },
  getters: {
    isAgentLoading: (state) => (agentType) => {
      return state.loading[agentType] || false
    },
    productionAgents: (state) => state.agentTypes.filter(a => 
      ['business_logic_policy', 'product_requirements', 'api_contract', 
       'technical_architecture', 'quality_test', 'change_impact', 
       'release_readiness'].includes(a.value)
    ),
    legacyAgents: (state) => state.agentTypes.filter(a => 
      !['business_logic_policy', 'product_requirements', 'api_contract', 
        'technical_architecture', 'quality_test', 'change_impact', 
        'release_readiness'].includes(a.value)
    )
  }
}
