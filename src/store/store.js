import Vue from 'vue'
import Vuex from 'vuex'
import VueSession from 'vue-session'
import api from './api.js'
import router from '../router'

Vue.use(Vuex)
Vue.use(VueSession)

const apiRoot = 'http://127.0.0.1:8000'  // This will change if you deploy later

const store = new Vuex.Store({
  state: {
    schema: '',
    credentials: {
      username: 'ruby',
      password: 'ruby'
    },
    configuration: {
      enableConfigure: false
    },
    currentPage: 'dashboard',
    series: [],
    dashboardChart: {
      series: [
        [[Date.UTC(2017, 9, 2), 0],
        [Date.UTC(2017, 9, 6), 0.25],
        [Date.UTC(2017, 9, 9), 1.41],
        [Date.UTC(2017, 9, 15), 1.64],
        [Date.UTC(2017, 9, 24), 1.6],
        [Date.UTC(2017, 9, 28), 2.55],
        [Date.UTC(2017, 9, 30), 2.81]],
        [[Date.UTC(2017, 9, 1), 3.25],
          [Date.UTC(2017, 9, 7), 1.66],
          [Date.UTC(2017, 9, 8), 1.8],
          [Date.UTC(2017, 9, 9), 1.76],
          [Date.UTC(2017, 9, 11), 2.62],
          [Date.UTC(2017, 9, 12), 2.41],
          [Date.UTC(2017, 9, 12), 2.05],
          [Date.UTC(2017, 9, 14), 1.7],
          [Date.UTC(2017, 9, 24), 1.1],
          [Date.UTC(2017, 9, 27), 0]
        ],
        [
          [Date.UTC(2017, 9, 1), 0],
          [Date.UTC(2017, 9, 3), 0.25],
          [Date.UTC(2017, 9, 5), 1.41],
          [Date.UTC(2017, 9, 7), 1.64],
          [Date.UTC(2017, 9, 8), 1.6],
          [Date.UTC(2017, 9, 12), 2.55],
          [Date.UTC(2017, 9, 13), 2.62],
          [Date.UTC(2017, 9, 17), 2.5],
          [Date.UTC(2017, 9, 19), 2.42],
          [Date.UTC(2017, 9, 20), 2.74],
          [Date.UTC(2017, 9, 21), 2.62],
          [Date.UTC(2017, 9, 21), 2.6],
          [Date.UTC(2017, 9, 22), 2.81],
          [Date.UTC(2017, 9, 23), 2.63],
          [Date.UTC(2017, 9, 30), 2.77]],
        [[Date.UTC(2017, 9, 1), 0],
            [Date.UTC(2017, 9, 4), 0.28],
            [Date.UTC(2017, 9, 6), 0.25],
            [Date.UTC(2017, 9, 7), 0.2],
            [Date.UTC(2017, 9, 12), 0.28],
            [Date.UTC(2017, 9, 16), 0.28],
            [Date.UTC(2017, 9, 20), 0.47],
            [Date.UTC(2017, 9, 21), 0.79],
            [Date.UTC(2017, 9, 26), 0.72],
            [Date.UTC(2017, 9, 30), 1.02]]
      ]
    }
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
    'LOGIN': function (state, response) {
      if (response.body.STATUS === 'SUCCESS') {
        Vue.toast('Login successful', {
          id: 'my-toast',
          className: ['toast-success'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 2000,
          mode: 'queue',
          transition: 'my-transition'
        })
        router.push({name: 'dashboard', params: { setSession: true }})
        state.currentPage = 'dashboard'
        state.credentials.username = response.body.username
      } else {
        Vue.toast('Login attempt failed', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 4000,
          mode: 'queue',
          transition: 'my-transition'
        })
      }
    },
    'LOGOUT': function (state, response) {
      if (response.body.STATUS === 'SUCCESS') {
        Vue.toast('Logged out successfully', {
          id: 'my-toast',
          className: ['toast-success'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 2000,
          mode: 'queue'
        })
        router.push('/login')
        state.currentPage = 'login'
        state.credentials.username = ''
      }
    },
    'DASHBOARD_DETAILS': function (state, response) {
      state.currentPage = 'dashboard'
      state.series = response.body
    },
    'DASHBOARD_CHART_INIT': function (state, response) {
      // works for one docker component
      console.log(response.body)
      var iniSeries = response.body
      var newSeries = []
      var temp = 0
      for (var i = 0; i < iniSeries.length; i++) {
        temp = iniSeries[i].splice(1)
        console.log(temp)
        temp[1] = parseInt(temp[1].substring(0, temp[1].length - 1))
        newSeries.push(temp)
      }
      console.log(newSeries)
      state.dashboardChart.series = [newSeries]
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
        .then((response) => store.commit('LOGIN', response))
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
    },
    logout (state, credentials) {
      var logout = {
        _action: 'logout',
        username: credentials.username
      }
      return api.post(apiRoot + '/index.html', logout)
        .then((response) => store.commit('LOGOUT', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    getDashboardCards (state) {
      var logout = {
        _action: 'getDashboardCards'
      }
      return api.post(apiRoot + '/index.html', logout)
        .then((response) => store.commit('DASHBOARD_DETAILS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    getDashboardChart (state) {
      var logout = {
        _action: 'getDashboardChart'
      }
      return api.post(apiRoot + '/index.html', logout)
        .then((response) => store.commit('DASHBOARD_CHART_INIT', response))
        .catch((error) => store.commit('API_FAIL', error))
    }
  }
})

export default store
