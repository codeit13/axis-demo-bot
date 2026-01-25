/** Change Impacts Vuex module */
import api from '../../services/api'

const state = {
  impacts: [],
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
  SET_IMPACTS(state, impacts) {
    state.impacts = impacts
  }
}

const actions = {
  async fetchChangeImpacts({ commit }, projectId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await api.getChangeImpacts(projectId)
      commit('SET_IMPACTS', response.data)
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
  impactsByProject: (state) => (projectId) => {
    return state.impacts.filter(i => i.project_id === projectId)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
