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
            <div>dApps Console</div>
        </div>
        <div @click="tabSwitch('stats')">
            <img src="../../assets/images/icon-server-b.svg"/>
            <div>dApps Stats</div>
        </div>
        <div @click="tabSwitch('threads')">
            <img src="../../assets/images/icon-thread-b.svg"/>
            <div>Threads</div>
        </div>
        <div class='registration-text'>Registered to:
            <div class='registered-user'>{{username}}</div>
        </div>
        <div class='versioning-info'>
            <span class='titania_version'>Titania {{this.$store.state.schema}} <br/></span>
            <span class='copyright'>Copyright {{new Date().getFullYear()}} Libertaria</span>  
        </div>
        <div @click="logout()" class='logout-menu'>
            <img src='../../assets/images/logout-icon.svg'/>
        </div>
    </div>
  </div>
</template>

<script>
import headerParent from '@/components/headerParent'
import router from '../../router'

export default {
  name: 'menu',
  computed: {
    page () {
      return 'MENU'
    },
    username: {
      get: function () {
        return this.$store.state.credentials.username
      }
    },
    currentPage: {
      get: function () {
        return this.$store.state.currentPage
      },
      set: function (page) {
        this.$store.state.currentPage = page
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
      if (tabname.length === 0) {
        router.push('/')
        this.$store.dispatch('switchDrilldown', 'dashboard')
      } else {
        router.push('/' + tabname)
        this.$store.dispatch('switchDrilldown', tabname)
        this.currentPage = tabname
      }
    }
  }
}
</script>
