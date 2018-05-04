<template>
  <div>
    <headerParent :name-prop="page"></headerParent>
    <div class='menu-page-wrapper'>
        <div @click="tabSwitch('')" >
            <img src="../../assets/images/titania-logo-white.svg"/>
            <div>Dashboard</div>
        </div>
        <div @click="tabSwitch('dappsconsole')">
            <img src="../../assets/images/icon-boxes-b.svg"/>
            <div>Console</div>
        </div>
        <div @click="tabSwitch('stats')">
            <img src="../../assets/images/icon-server-b.svg"/>
            <div>Stats</div>
        </div>
        <div @click="tabSwitch('threads')">
            <img src="../../assets/images/icon-thread-b.svg"/>
            <div>Threads</div>
        </div>
        <div @click="tabSwitch('dappshub')">
            <img src="../../assets/images/icon-hub-b.svg"/>
            <div>Hub</div>
        </div>
        <div class='registration-text'>Logged in as:<div class='registered-user'>{{username}}</div></div>
        <div class='registration-text'>Box name:<div class='registered-user'>{{boxname}}</div></div>
        <div class='versioning-info'>
            <span class='titania_version'>
              <a @click="getHashDetails()">{{this.$store.state.schema}}</a>
            </span>
            <br/>
            <span class='copyright'>Copyright {{new Date().getFullYear()}} Libertaria</span>  
        </div>
        <div @click="tabSwitch('settings')" class='settings-menu'>
            <img src='../../assets/images/settings-gray.svg'/>
        </div>
        <div @click="logout()" class='logout-menu'>
            <img src='../../assets/images/logout-icon.svg'/>
        </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import headerParent from '@/components/common/headerParent'
import router from '../../router'

Vue.use(VueLocalStorage)

export default {
  name: 'menu',
  computed: {
    page () {
      return 'MENU'
    },
    username: {
      get: function () {
        if (this.$store.state.currentPage === 'configure') {
          return true
        }
        return Vue.ls.get('user')
      }
    },
    boxname: {
      get: function () {
        if (this.$store.state.currentPage === 'configure') {
          return true
        }
        // console.log(Vue.ls.get('boxname'))
        return Vue.ls.get('boxname')
      }
    },
    currentPage: {
      get: function () {
        return this.$store.state.currentPage
      },
      set: function (page) {
        this.$store.state.currentPage = page
      }
    },
    hashPopupState: {
      get: function () {
        return this.$store.state.hashPopupState
      },
      set: function (newstate) {
        this.$store.state.hashPopupState = newstate
      }
    }
  },
  components: {
    headerParent
  },
  mounted: function () {
  },
  methods: {
    logout () {
      this.$session.destroy()
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    },
    tabSwitch (tabname) {
      this.$store.state.menu = !this.$store.state.menu
      if (tabname.length === 0) {
        router.push('/')
        this.$store.dispatch('switchDrilldown', 'dashboard')
      } else {
        router.push('/' + tabname)
        this.$store.dispatch('switchDrilldown', tabname)
        this.currentPage = tabname
      }
    },
    getHashDetails () {
      this.hashPopupState = !this.hashPopupState
    }
  }
}
</script>
