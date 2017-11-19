<div class='sidebar-container dark-black'>
</div>

<template>
  <div class='sidebar-container dark-black'>
    <div @click="tabSwitch('')">
      <img class="logo-icon-small" src="../assets/images/titania-logo.png">
    </div>
    <div class='margin-top-20' @click="tabSwitch('dappsconsole')" v-bind:class="{ activeDrilldown: currentTab('dappsconsole')}">
      <img class="tab-label" src="../assets/images/docker-tab.png">
    </div>
    <div @click="tabSwitch('sometab')">
      <img class="tab-label" src="../assets/images/uptime.png">
    </div>
    <div @click="tabSwitch('systemhealth')">
      <img class="tab-label" src="../assets/images/neigh_nodes.png">
    </div>
    <div @click="tabSwitch('Config')">
      <img class="tab-label" src="../assets/images/tab-thread.png">
    </div>
  </div>
</template>

<script>
import router from '../router'

export default {
  name: 'sidebarParent',
  computed: {
    currentPage: {
      get () {
        return this.$store.state.currentPage
      }
    }
  },
  methods: {
    tabSwitch (tabname) {
      if (tabname.length === 0) {
        router.push('/')
        this.$store.dispatch('switchDrilldown', 'dashboard')
      } else {
        router.push('/' + tabname)
        this.$store.dispatch('switchDrilldown', tabname)
      }
    },
    currentTab (tabname) {
      return this.currentPage === tabname
    }
  }
}
</script>
