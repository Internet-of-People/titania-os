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
    <div @click="tabSwitch('sometab')" v-bind:class="{ activeDrilldown: currentTab('sometab')}">
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
  methods: {
    tabSwitch (tabname) {
      router.push('/' + tabname)
      this.$store.dispatch('switchDrilldown', tabname)
    },
    currentTab (tabname) {
      return this.$store.state.currentPage === tabname
    }
  }
}
</script>
