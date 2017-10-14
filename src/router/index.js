import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import configure from '@/components/configuration/configure'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/configure',
      name: 'configure',
      component: configure
    }
  ]
})
