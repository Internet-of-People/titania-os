// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/store.js'
import VueHighcharts from 'vue-highcharts'
import Toast from 'vue-easy-toast'
import VueSession from 'vue-session'

Vue.use(VueSession)
Vue.use(Toast)
Vue.use(VueHighcharts)

Vue.config.productionTip = false

/* eslint-disable no-new */
const v = new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})

v.$store.dispatch('initApp')
