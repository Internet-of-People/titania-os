import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'
import router from '../router'

Vue.use(Vuex)
const apiRoot = 'http://localhost:8000'  // This will change if you deploy later

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
    // Keep in mind that response is an HTTP response
    // returned by the Promise.
    // The mutations are in charge of updating the client state.
    'GET_CREDS': function (state, response) {
      if (response.body.length === 0) {
        console.log('login has not been set')
        router.push('/configure')
      }
    },
    'CLEAR_TODOS': function (state) {
      const todos = state.todos
      todos.splice(0, todos.length)
    },
    // Note that we added one more for logging out errors.
    'API_FAIL': function (state, error) {
      console.error(error)
    }
  },
  actions: {
    getCreds (store) {
      return api.get(apiRoot + '/configinfo/')
        .then((response) => store.commit('GET_CREDS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    clearTodos (store) {
      return api.delete(apiRoot + '/configinfo/clear_todos/')
        .then((response) => store.commit('CLEAR_TODOS'))
        .catch((error) => store.commit('API_FAIL', error))
    },
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
  }
})

export default store
