/** Business Rules Vuex module */
import api from '../../services/api'

const state = {
  rules: [],
  currentRule: null,
  ruleVersions: [],
  loading: false,
  error: null
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_RULES(state, rules) {
    state.rules = rules
  },
  ADD_RULE(state, rule) {
    state.rules.unshift(rule)
  },
  UPDATE_RULE(state, updatedRule) {
    const index = state.rules.findIndex(r => r.rule_id === updatedRule.rule_id)
    if (index !== -1) {
      state.rules[index] = updatedRule
    }
  },
  SET_CURRENT_RULE(state, rule) {
    state.currentRule = rule
  },
  SET_RULE_VERSIONS(state, versions) {
    state.ruleVersions = versions
  }
}

const actions = {
  async fetchRules({ commit }, projectId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.getBusinessRules(projectId)
      commit('SET_RULES', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createRule({ commit }, { projectId, rule }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.createBusinessRule(projectId, rule)
      commit('ADD_RULE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async getRule({ commit }, ruleId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.getBusinessRule(ruleId)
      commit('SET_CURRENT_RULE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateRule({ commit }, { ruleId, rule }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.updateBusinessRule(ruleId, rule)
      commit('UPDATE_RULE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async approveRule({ commit }, { ruleId, approvedBy }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.approveBusinessRule(ruleId, approvedBy)
      commit('UPDATE_RULE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchRuleVersions({ commit }, ruleId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.getRuleVersions(ruleId)
      commit('SET_RULE_VERSIONS', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  approvedRules: (state) => state.rules.filter(r => r.status === 'approved'),
  pendingRules: (state) => state.rules.filter(r => r.status === 'pending_approval'),
  draftRules: (state) => state.rules.filter(r => r.status === 'draft'),
  ruleById: (state) => (ruleId) => state.rules.find(r => r.rule_id === ruleId)
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
