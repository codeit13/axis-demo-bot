import { createStore } from 'vuex'
import projects from './modules/projects'
import agents from './modules/agents'
import suggestions from './modules/suggestions'
import issues from './modules/issues'
import businessRules from './modules/businessRules'
import changeImpacts from './modules/changeImpacts'

export default createStore({
  modules: {
    projects,
    agents,
    suggestions,
    issues,
    businessRules,
    changeImpacts
  }
})
