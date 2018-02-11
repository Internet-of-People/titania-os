<template>
  <div class="header-inner-wrapper">
    <div class="page-title sans-serif-normal float-left regular-fontsize">{{getPageTitle(nameProp)}}</div>
    <div class="display-inline-flex float-right">
      <div v-if="otherAddons.length > 0" @click="showServices()" title="Services" class="services-menu">
        <img src='../../assets/images/apps-icon.svg'>
      </div>
      <div @click="logout()" class="toolbar-header-options cursor-pointer">
        LOGOUT
      </div>
      <div class='hide-mobile-menu' @click="openMenu()">
        <img src='../../assets/images/menu-icon.svg'>
      </div>
    </div>
    <!-- <div v-if="services" class='services-dropdown-menu'>
      <div v-for="item in otherAddons" :key="item.id" class="display-inline-flex service-item">
        <div class=""  :title="item.name">
          <a class="" :href="item.address" target='_blank'>
            <img src='../../assets/images/defaultAppIcon1b.svg'>
            <div class="service-name">{{item.name}}</div>
          </a>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'

Vue.use(VueLocalStorage)

export default {
  name: 'headerParent',
  props: ['nameProp'],
  computed: {
    otherAddons: {
      get: function () {
        return this.$store.state.sidebarAddons
      }
    }
    // ,
    // services: {
    //   get: function () {
    //     return this.$store.state.services
    //   },
    //   set: function (val) {
    //     this.$store.state.services = val
    //   }
    // }
  },
  methods: {
    logout () {
      this.$session.destroy()
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
      this.$store.state.credentials.password = ''
      Vue.ls.set('user', '')
    },
    getPageTitle (pagename) {
      return pagename === 'DASHBOARD' ? 'DASHBOARD' : 'DASHBOARD  >  ' + pagename
    },
    openMenu () {
      if (this.$store.state.menu) {
        this.$router.push('/')
      } else {
        this.$router.push('/menu')
      }
      this.$store.state.menu = !this.$store.state.menu
    },
    showServices () {
      // console.log(this)
      // this.services = !this.services
    }
  },
  mounted: function () {
    // console.log(Vue.ls.get('user'))
  }
}
</script>
