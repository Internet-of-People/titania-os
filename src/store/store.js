import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'
import router from '../router'

Vue.use(Vuex)
const apiRoot = 'http://localhost:8000'  // This will change if you deploy later

const store = new Vuex.Store({
  state: {
    schema: '',
    credentials: {
      username: 'Tatia',
      password: ''
    },
    configuration: {
      enableConfigure: false
    },
    currentPage: 'dashboard'
  },
  mutations: {
    // Keep in mind that response is an HTTP response
    // returned by the Promise.
    // The mutations are in charge of updating the client state.
    'SET_SCHEMA': function (state, response) {
      state.schema = response.body[0].version
    },
    'GET_CREDS': function (state, response) {
      if (response.body.length === 0) {
        console.log('login has not been set')
        router.push('/configure')
        state.currentPage = 'configure'
      } else {
        router.push('/login')
        state.currentPage = 'login'
      }
    },
    'TOGGLE_CONFIGURATION': function (state) {
      state.configuration.enableConfigure = !state.configuration.enableConfigure
    },
    'SAVE_CONFIGURATION': function (state, response) {
      router.push('/login')
      state.currentPage = 'login'
    },
    'LOGIN_SUCCESS': function (state) {
      router.push('/')
      state.currentPage = 'dashboard'
    },
    // Note that we added one more for logging out errors.
    'API_FAIL': function (state, error) {
      console.error(error)
    },
    'SET_CURRENT_PAGE': function (state, pageName) {
      state.currentPage = pageName
    }
  },
  actions: {
    initApp (state) {
      var getSchema = {
        _action: 'getSchema'
      }
      return api.post(apiRoot + '/index.html', getSchema)
        .then(function (response) {
          store.commit('SET_SCHEMA', response)
          store.dispatch('getCreds')
        }).catch((error) => store.commit('API_FAIL', error))
    },
    getCreds (state) {
      var getUserDetails = {
        _action: 'getUserDetails'
      }
      return api.post(apiRoot + '/index.html', getUserDetails)
        .then((response) => store.commit('GET_CREDS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    // clearTodos (store) {
    //   return api.delete(apiRoot + '/schema/clear_todos/')
    //     .then((response) => store.commit('CLEAR_TODOS'))
    //     .catch((error) => store.commit('API_FAIL', error))
    // },
    login (state, credentials) {
      var login = {
        _action: 'login',
        username: credentials.username,
        password: credentials.password
      }
      return api.post(apiRoot + '/index.html', login)
        .then((response) => store.commit('LOGIN_SUCCESS', response))
        .catch((error) => store.commit('API_FAIL', error))
      // write code to check session id, store it in backend
    },
    toggleConfigForm (state) {
      store.commit('TOGGLE_CONFIGURATION')
    },
    saveConfigForm (state, configdetails) {
      configdetails._action = 'saveUserDetails'
      return api.post(apiRoot + '/index.html', configdetails)
        .then((response) => store.commit('SAVE_CONFIGURATION', configdetails))
        .catch((error) => store.commit('API_FAIL', error))
    }
  }
})

export default store
