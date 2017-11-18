import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import configure from '@/components/configuration/configure'
import dashboard from '@/components/dashboard/dashboardParent'
import dappsParent from '@/components/dappsconsole/dappsParent'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: dashboard,
      props: { showLogin: true }
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/configure',
      name: 'configure',
      component: configure
    },
    {
      path: '/dappsconsole',
      name: 'dappsconsole',
      component: dappsParent
    }
  ]
})
