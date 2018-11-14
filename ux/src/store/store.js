import Vue from 'vue'
import Vuex from 'vuex'
import VueSession from 'vue-session'
import VueLocalStorage from 'vue-ls'
import api from './api.js'
import router from '../router'
import { isNull } from 'util';

Vue.use(Vuex)
Vue.use(VueSession)
Vue.use(VueLocalStorage)

const apiRoot = '/api' // deployment
// const apiRoot = 'http://127.0.0.1:8000' // dev mac
// const apiRoot = 'http://192.168.1.194:8000' // dev pi

const local_store = Vue.ls

const store = new Vuex.Store({
  state: {
    schema: '',
    build_id: '',
    // ux_id: '',
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
    dappsjson: [],    
    hashPopupState: false,
    showupdatepopup: false,
    updateState: 'initial', /**States: initial, updating, success, failure */
    updateData: {},
    dappsFilter: 'AVAILABLE',
    showdappdetail: false,
    activedapp: {},
    activecategory: 'helper',
    natpmp: 1,
    updatedapps: [],
    dappstates: {
      enabled_and_active: 1,
      disabled: 0,
      not_downloaded: -1,
      downloading: 2,
      enabled_and_not_active: 3
    }
  },
  mutations: {
    // Keep in mind that response is an HTTP response
    // returned by the Promise.
    // The mutations are in charge of updating the client state.
    'SET_SCHEMA': function (state, response) {
      state.schema = response.body.version
      state.build_id = response.body.build_id
      // state.ux_id = response.body.ux_id
    },
    'GET_CREDS': function (state, response) {
      if (response.body.configState) {
        if (router.currentRoute.path == '/configure' || router.currentRoute.path == '/landingpage') {
          router.push({name: 'login', params: { deletesession: true }})
          state.currentPage = 'login'
        }
      } else {
        router.push('/configure')
        state.currentPage = 'configure'
      }
    },
    'GET_ALL_APS': function (state, response) {
      // response.body = []
      state.configuration.wifi_aps = response.body
      state.configuration.wifi_aps_current = response.body[0][0]
      // router.push('/configure')
      // state.currentPage = 'configure'
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
        // console.log(response.body.session_key)
        Vue.toast('Login successful', {
          id: 'my-toast',
          className: ['toast-success'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 3000,
          mode: 'queue',
          transition: 'my-transition'
        })
        router.push({name: 'dashboard', params: { setSession: true }})
        state.currentPage = 'dashboard'
        state.credentials.username = response.body.username
        local_store.set('user', state.credentials.username)
        local_store.set('session_key_'+state.credentials.username, response.body.session_key)
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
      if (error.status === 0 || error.status === 502) {
        state.currentPage = 'landingpage'
        router.push('/landingpage')
        setTimeout(function () {
          location.reload()
        }, 8000)
      } else if (error.status === 302) {
        var user = local_store.get('user')
        local_store.remove('system_key'+user)
        local_store.remove('user')
        if (state.currentPage != 'login') {
          router.push({name: 'login', params: { deletesession: true }})
          state.currentPage = 'login'
          state.credentials.username = ''
          state.credentials.password = ''
        }
      }
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
    'UPDATE_STATUS': function (state, response) { 
      state.updateState = response.body.STATUS
      // Case of login/configure/landing refresh, where call doesnt contain the generated session key
      if (response.body.STATUS == 'FAILURE') {
        state.updateState = 'initial'
      }
      if (state.updateState == 'updating') {
        state.updateData = response.body.data
        setTimeout(function () {
          store.dispatch('getUpdateStatus')
        }, 4000)
      } else if (state.updateState == 'success' || state.updateState == 'failure') {
        var popup = local_store.get('update_popup')?local_store.get('update_popup'):null
        if (isNull(popup)) {
          local_store.set('update_popup', true)
          state.showupdatepopup = true
        }
        state.updateData = {}
      } else {
        state.updateData = {}
      }
    },
    'SET_UPDATE_INIT': function (state, imagename) {
      local_store.set('update_img', imagename)
      state.updateState = 'updating'
    },
    'SET_INITIAL_UPDATE_STATUS': function (state) {
      state.updateState = 'initial'
      local_store.remove('update_popup')
      local_store.remove('update_img')
    },
    'INIT_DAPP_STORE': function (state, response) {
      state.dappsjson = []
      state.dappsjson = response.body.dapps_store
    },
    'SET_DAPP_LIST_NULL': function (state) {
      state.dappsjson = []
    },
    'NATPMP_STATUS': function (state, response) {
      if (response.body.STATUS != 'FAILURE') {
        state.natpmp = response.body.STATUS
      }
    },
    'SET_UPDATE_FLAGS': function (state, response) {
      state.updatedapps = response.body.update_list
    },
    'SET_REBOOT_SCREEN': function (state) {
      router.push({name: 'landingpage', params: { reboot: true }})
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
          store.dispatch('getUpdateStatus')
          store.dispatch('getNatpmpStatus')
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
        .then(function (response) {
          store.commit('LOGIN', response)
          store.dispatch('getUpdateStatus')
          store.dispatch('getNatpmpStatus')
        }).catch((error) => store.commit('API_FAIL', error))
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
      configdetails.wifi_encrpt = store.state.configuration.wifi_encrpt
      return api.post(apiRoot + '/index.html', configdetails)
        .then((response) => store.commit('SAVE_CONFIGURATION', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    logout (state, credentials) {
      var logout = {
        _action: 'logout',
        username: credentials.username
      }
      return api.postWithSession(apiRoot + '/index.html', logout)
        .then((response) => store.commit('LOGOUT', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    getDashboardCards (state) {
      var dashboardcards = {
        _action: 'getDashboardCards'
      }
      return api.postWithSession(apiRoot + '/index.html', dashboardcards)
        .then((response) => store.commit('DASHBOARD_DETAILS', response))
        .catch((error) => store.commit('API_FAIL', error))
    },
    getDashboardChart (state) {
      var dashboardchart = {
        _action: 'getDashboardChart'
      }
      return api.postWithSession(apiRoot + '/index.html', dashboardchart)
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
      return api.postWithSession(apiRoot + '/index.html', dockeroverview)
      .then((response) => store.commit('DOCKER_OVERVIEW', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getContainerStats (state) {
      var getStats = {
        _action: 'getContainerStats'
      }
      return api.postWithSession(apiRoot + '/index.html', getStats)
      .then((response) => store.commit('DOCKER_STATS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getThreads (state) {
      var threads = {
        _action: 'getThreads'
      }
      return api.postWithSession(apiRoot + '/index.html', threads)
      .then((response) => store.commit('DOCKER_THREADS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getContainerTop (state) {
      var containerthreads = {
        _action: 'getContainerTop'
      }
      return api.postWithSession(apiRoot + '/index.html', containerthreads)
      .then((response) => store.commit('CONTAINER_THREADS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    getSettingsList (state) {
      var settings = {
        _action: 'getSettings'
      }
      return api.postWithSession(apiRoot + '/index.html', settings)
      .then((response) => store.commit('SETTINGS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    deleteUser (state, deleterequest) {
      deleterequest._action = 'deleteUser'
      return api.postWithSession(apiRoot + '/index.html', deleterequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    addNewUser (state, configdetails) {
      configdetails._action = 'addNewUser'
      return api.postWithSession(apiRoot + '/index.html', configdetails)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    addWifi (state, configdetails) {
      configdetails._action = 'addWifi'
      configdetails.wifi_encrpt = store.state.configuration.wifi_encrpt
      return api.postWithSession(apiRoot + '/index.html', configdetails)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    deleteWifi (state, deleterequest) {
      deleterequest._action = 'deleteWifi'
      return api.postWithSession(apiRoot + '/index.html', deleterequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    editWifi (state, editrequest) {
      editrequest._action = 'editWifi'
      return api.postWithSession(apiRoot + '/index.html', editrequest)
      .then((response) => store.commit('REFRESH_LIST', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    updateOSImage (state) {
      var formData = new FormData()
      var updateDiv = document.getElementById('updateInput')
      var update_img = updateDiv.files[0]
      var user = local_store.get('user')
      var session_key = local_store.get('session_key_'+user)
      formData.append('file', update_img, update_img.name)
      formData.append('_action', 'updateOSImage')
      formData.append('session_key', session_key)
      store.commit('SET_UPDATE_INIT', update_img.name)
      
      return api.postWithSessionAndUpload(apiRoot + '/index.html', formData)
      .then(function (response) {
        store.dispatch('getUpdateStatus')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    getUpdateStatus (state) {
      var updatestatus = {
        _action: 'getUpdateStatus'
      }
      var update_img = local_store.get('update_img')?local_store.get('update_img'):""
      if (update_img.length > 0) {
        updatestatus.image_name = update_img
        return api.postWithSession(apiRoot + '/index.html', updatestatus)
        .then((response) => store.commit('UPDATE_STATUS', response))
        .catch((error) => store.commit('API_FAIL', error))
      } else {
        store.commit('SET_INITIAL_UPDATE_STATUS', {})
      }
    },
    rebootSystem (state) {
      var rebootSystem = {
        _action: 'rebootSystem'
      }
      $('body').css('cursor', 'progress')
      Vue.toast('Restarting TitaniaOS', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      store.commit('SET_INITIAL_UPDATE_STATUS', {})
      return api.postWithSession(apiRoot + '/index.html', rebootSystem)
      .then(function (response) {
        $('body').css('cursor', 'default')
        $('#my-toast').remove()
        store.commit('SET_REBOOT_SCREEN')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    retryUpdate (state) {
      store.commit('SET_INITIAL_UPDATE_STATUS', {})
    },
    fetchAlldApps (state) {
      var fetchAlldApps = {
        _action: 'fetchAlldApps'
      }
      return api.postWithSession(apiRoot + '/index.html', fetchAlldApps)
      .then(function (response) {
        store.commit('INIT_DAPP_STORE', response)
      }).catch((error) => store.commit('API_FAIL', error))
    },
    fetchUpdatableDapps (state) {
      var fetchUpdatableDapps = {
        _action: 'fetchUpdatableDapps'
      }
      return api.postWithSession(apiRoot + '/index.html', fetchUpdatableDapps)
      .then((response) => store.commit('SET_UPDATE_FLAGS', response))
      .catch((error) => store.commit('API_FAIL', error))
    },
    disableDapp(state, dappid) {
      var disableDapp = {
        _action: 'disableDapp'
      }
      disableDapp.id = dappid
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Disabling dapp and fetching updated list', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', disableDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    enableDapp(state, dappid) {
      var enableDapp = {
        _action: 'enableDapp'
      }
      enableDapp.id = dappid
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Enabling dapp and fetching updated list', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', enableDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    restartDapp(state, dappid) {
      var restartDapp = {
        _action: 'restartDapp'
      }
      restartDapp.id = dappid
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Restarting dapp and fetching updated list', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', restartDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    removeDapp(state, dapp) {
      var removeDapp = {
        _action: 'removeDapp'
      }
      removeDapp.id = dapp.id
      removeDapp.image = dapp.image
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Removing dapp ' + dapp.name + ' and fetching updated list', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', removeDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    downloadDapp(state, dapp) {
      var downloadDapp = {
        _action: 'downloadDapp'
      }
      downloadDapp.id = dapp.id
      downloadDapp.image = dapp.image
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Downloading dapp ' + dapp.name + ' and fetching updated list \n This may take some time.', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', downloadDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    updateDapp(state, dappid) {
      var updateDapp = {
        _action: 'updateDapp'
      }
      updateDapp.id = dappid
      $('#hub-loader').removeClass('hide')
      $('body').css('cursor', 'progress')
      Vue.toast('Updating dapp and fetching updated list', {
        id: 'my-toast',
        className: ['toast-info'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
        duration: 40000,
        mode: 'queue'
      })
      return api.postWithSession(apiRoot + '/index.html', updateDapp)
      .then(function (response) {
        $('#hub-loader').addClass('hide')
        $('#my-toast').remove()
        $('body').css('cursor', 'default')
        store.commit('SET_DAPP_LIST_NULL')
        store.dispatch('fetchAlldApps')
      }).catch((error) => store.commit('API_FAIL', error))
    },
    getNatpmpStatus (state) {
      var natpmpstatus = {
        _action: 'getNatpmpStatus'
      }
      return api.postWithSession(apiRoot + '/index.html', natpmpstatus)
      .then((response) => store.commit('NATPMP_STATUS', response))
      .catch((error) => store.commit('API_FAIL', error))
    }
  }
})

export default store
