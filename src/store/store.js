import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
  state: {
    credentials: {
      username: 'Tatia',
      password: ''
    },
    configuration: {
      enableConfigure: false
    }
  },
  mutations: {
    login (state) {
      console.log(state.credentials.username + state.credentials.password)
    },
    openConfigForm (state) {
      state.configuration.enableConfigure = true
    },
    closeConfigForm (state) {
      state.configuration.enableConfigure = false
    },
    saveConfigForm (state, configdetails) {
      console.log(configdetails)
      store.commit('closeConfigForm')
    }
  },
  actions: {
  }
})

export default store
