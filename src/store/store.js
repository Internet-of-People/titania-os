import Vue from 'vue'
import Vuex from 'vuex'
import VueSession from 'vue-session'
import api from './api.js'
import router from '../router'
import VueLocalStorage from 'vue-ls'

Vue.use(Vuex)
Vue.use(VueSession)
Vue.use(VueLocalStorage)

// const apiRoot = '/api' // deployment
// const apiRoot = 'http://127.0.0.1:8000' // dev mac
const apiRoot = 'http://192.168.0.105:8000' // dev pi

const store = new Vuex.Store({
  state: {
    schema: '',
    credentials: {
      username: '',
      password: ''
    },
    configuration: {
      wifi_aps: [],
      wifi_aps_current: '',
      wifi_encrpt: 'WPA (default)',
      tabname: 'config',
      enableConfigure: false
    },
    currentPage: 'dashboard',
    series: [],
    dashboardChart: {
      series: [],
      seriesname: []
    },
    dockeroverview: [],
    dockerstats: [],
    showDetails: 'Show details',
    dappsfilter: 'All',
    dropdownstate: false,
    threadfilter: 'all',
    threads: [],
    containerthreads: [],
    menu: 0,
    settingOption: 'users',
    settings: {
      users: [],
      wifi: [],
      getform: false,
      getaseditwifiform: false,
      editwifiap: ''
    },
    sidebarAddons: [],
    services: false,
    encrypt_modes: ['WPA (default)', 'Open', 'WEP'],
    showupdatepopup: false,
    updateState: 'initial' /**States: initial, update, success, failure */
  },
  mutations: {
    // Keep in mind that response is an HTTP response
    // returned by the Promise.
    // The mutations are in charge of updating the client state.
    'SET_SCHEMA': function (state, response) {
      state.schema = response.body.version_info
    },
    'GET_CREDS': function (state, response) {
      // console.log(response.body.configState)
      if (response.body.configState) {
        router.push('/login')
        state.currentPage = 'login'
        // Vue.ls.set('boxname', response.body[0].boxname)
      } else {
        router.push('/configure')
        state.currentPage = 'configure'
      }
    },
    'GET_ALL_APS': function (state, response) {
      // response.body = []
      state.configuration.wifi_aps = response.body
      state.configuration.wifi_aps_current = response.body[0][0]
      state.currentPage = 'configure'
    },
    'SAVE_CONFIGURATION': function (state, response) {
      // removing loaders
      $('body').css('cursor', 'default')
      $('#saveForm').css('cursor', 'pointer')
      // open login form
      if (response.body.STATUS === 'SUCCESS') {
        router.push('/login')
        state.currentPage = 'login'
      }
    },
    'LOGIN': function (state, response) {
      // removing loaders
      $('body').css('cursor', 'default')
      $('#login_submit').css('cursor', 'pointer')
      // applying response set
      if (response.body.username) {
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
        Vue.ls.set('user', state.credentials.username)
      } else {
        Vue.toast(response.body, {
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
      var iniSeries = response.body
      var newSeries = []
      var newSeriesName = []
      for (var i = 0; i < iniSeries.length; i++) {
        newSeriesName.push(iniSeries[i].container_name)
        newSeries.push(iniSeries[i].data)
      }
      state.dashboardChart.seriesname = newSeriesName
      state.dashboardChart.series = newSeries
    },
    // Note that we added one more for logging out errors.
    'API_FAIL': function (state, error) {
      state.currentPage = 'landingpage'
      router.push('/landingpage')
      if (error.status === 0 || error.status === 502) {
        setTimeout(function () {
          location.reload()
        }, 8000)
      }
      console.error(error.status)
    },
    'SET_CURRENT_PAGE': function (state, pageName) {
      state.currentPage = pageName
    },
    'DOCKER_OVERVIEW': function (state, response) {
      state.dockeroverview = response.body
    },
    'DOCKER_STATS': function (state, response) {
      state.dockerstats = response.body
    },
    'DOCKER_THREADS': function (state, response) {
      state.threads = response.body
    },
    'CONTAINER_THREADS': function (state, response) {
      state.containerthreads = response.body
    },
    'SETTINGS': function (state, response) {
      state.settings.users = response.body[0].users
      state.settings.wifi = response.body[0].wifi
      // verify no aps found case
      // state.configuration.wifi_aps = []
      // state.configuration.wifi_aps_current = ''
      state.configuration.wifi_aps = response.body[0].allwifiaps
      state.configuration.wifi_aps_current = response.body[0].allwifiaps[0][0]
    },
    'REFRESH_LIST': function (state, response) {
      // removing loaders
      $('body').css('cursor', 'default')
      $('#saveForm').css('cursor', 'pointer')
      $('.del-user').css('cursor', 'pointer')
      $('.del-wifi').css('cursor', 'pointer')
      var message = ''
      var reqtype = response.body[0].reqtype
      var endpoint = response.body[0].endpoint
      if (reqtype === 'addwifi') {
        message = 'Wifi ' + endpoint + ' setup successfully'
      } else if (reqtype === 'deletewifi') {
        message = 'Wifi ' + endpoint + ' removed successfully'
      } else if (reqtype === 'editwifi') {
        message = 'Wifi ' + endpoint + ' edited successfully'
      } else {
        message = reqtype === 'deleteuser' ? 'User ' + endpoint + ' deleted successfully' : 'User ' + endpoint + ' added successfully'
      }
      Vue.toast(message, {
        id: 'my-toast',
        className: ['toast-success'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 2000,
        mode: 'queue'
      })
      state.settings.users = response.body[0].users
      state.settings.wifi = response.body[0].wifi
      state.configuration.wifi_aps = response.body[0].allwifiaps
      state.configuration.wifi_aps_current = response.body[0].allwifiaps[0][0]
      state.settings.getform = false
    },
    'UPDATE_OS': function (state, response) {
      console.log('Wow, update chal gya')
    }
    // 'RECORD_ADDONS': function (state, response) {
    //   state.sidebarAddons = response.body
    //   // state.sidebarAddons = [{'id': 1, 'name': 'HelloWorld', 'address': 'http://192.168.2.5:3000', 'icon': 'willsupply'},
    //   // {'id': 2, 'name': 'iopwallet', 'address': 'http://192.168.2.5:3000', 'icon': 'willsupply'}]
    // }
  },
  actions: {
    // loadDependencies (state) {
    //   var loadDependencies = {
    //     _action: 'loadDependencies'
    //   }
    //   return api.post(apiRoot + '/index.html', loadDependencies)
    //   .then(function (response) {
    //     store.commit('RECORD_ADDONS', response)
    //   }).catch((error) => store.commit('API_FAIL', error))
    // },
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
      var getIfConfigured = {
        _action: 'getIfConfigured'
      }
      return api.post(apiRoot + '/index.html', getIfConfigured)
        .then((response) => store.commit('GET_CREDS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    login (state, credentials) {
      var login = {
        _action: 'login',
        username: escape(credentials.username),
        password: credentials.password
      }
      return api.post(apiRoot + '/index.html', login)
        .then((response) => store.commit('LOGIN', response))
        .catch((error) => store.commit('API_FAIL', error))
      // write code to check session id, store it in backend
    },
    getAllAPs (state) {
      var getAllAPs = {
        _action: 'getAllAPs'
      }
      return api.post(apiRoot + '/index.html', getAllAPs)
        .then((response) => store.commit('GET_ALL_APS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    saveConfigForm (state, configdetails) {
      configdetails._action = 'saveUserDetails'
      return api.post(apiRoot + '/index.html', configdetails)
        .then((response) => store.commit('SAVE_CONFIGURATION', response))
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
      var dashboardcards = {
        _action: 'getDashboardCards'
      }
      return api.post(apiRoot + '/index.html', dashboardcards)
        .then((response) => store.commit('DASHBOARD_DETAILS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    getDashboardChart (state) {
      var dashboardchart = {
        _action: 'getDashboardChart'
      }
      return api.post(apiRoot + '/index.html', dashboardchart)
        .then((response) => store.commit('DASHBOARD_CHART_INIT', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    switchDrilldown (state, tabname) {
      store.commit('SET_CURRENT_PAGE', tabname)
    },
    getDockerOverview (state) {
      var dockeroverview = {
        _action: 'getDockerOverview'
      }
      return api.post(apiRoot + '/index.html', dockeroverview)
      .then((response) => store.commit('DOCKER_OVERVIEW', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getContainerStats (state) {
      var getStats = {
        _action: 'getContainerStats'
      }
      return api.post(apiRoot + '/index.html', getStats)
      .then((response) => store.commit('DOCKER_STATS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getThreads (state) {
      var threads = {
        _action: 'getThreads'
      }
      return api.post(apiRoot + '/index.html', threads)
      .then((response) => store.commit('DOCKER_THREADS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getContainerTop (state) {
      var containerthreads = {
        _action: 'getContainerTop'
      }
      return api.post(apiRoot + '/index.html', containerthreads)
      .then((response) => store.commit('CONTAINER_THREADS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getSettingsList (state) {
      var settings = {
        _action: 'getSettings'
      }
      return api.post(apiRoot + '/index.html', settings)
      .then((response) => store.commit('SETTINGS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    deleteUser (state, deleterequest) {
      deleterequest._action = 'deleteUser'
      return api.post(apiRoot + '/index.html', deleterequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    addNewUser (state, configdetails) {
      configdetails._action = 'addNewUser'
      return api.post(apiRoot + '/index.html', configdetails)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    addWifi (state, configdetails) {
      configdetails._action = 'addWifi'
      return api.post(apiRoot + '/index.html', configdetails)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    deleteWifi (state, deleterequest) {
      deleterequest._action = 'deleteWifi'
      return api.post(apiRoot + '/index.html', deleterequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    editWifi (state, editrequest) {
      editrequest._action = 'editWifi'
      return api.post(apiRoot + '/index.html', editrequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    updateOSImage (state) {
      var formData = new FormData()
      var updateDiv = document.getElementById('updateInput')
      formData.append('file', updateDiv.files[0],updateDiv.files[0].name)
      formData.append('_action', 'updateOSImage')
      
      return api.postWithUpload(apiRoot + '/index.html', formData)
      .then((response) => store.commit('UPDATE_OS', response))
      .catch((error) => store.commit('API_FAIL', error))
      console.log(updateDiv.files[0])
    }
  }
})

export default store
