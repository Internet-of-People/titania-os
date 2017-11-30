<div class='sidebar-container dark-black'>
</div>

<template>
  <div class='sidebar-container dark-black'>
    <div @click="tabSwitch('')" title='Dashboard'>
      <img class="logo-icon-small cursor-pointer" src="../assets/images/titania-logo-clean.svg">
    </div>
    <div class='margin-top-20 cursor-pointer' title='dApps Console' @click="tabSwitch('dappsconsole')" >
      <img v-if="currentTab('dappsconsole')" class="tab-label" src="../assets/images/dApps-selected.svg">
      <img v-else class="tab-label" src="../assets/images/dApps-icon.svg">
    </div>
    <div @click="tabSwitch('stats')" title='dApps Stats' class='cursor-pointer'>
      <img v-if="currentTab('stats')" class="tab-label" src="../assets/images/uptime-selected.svg">
      <img v-else class="tab-label" src="../assets/images/uptime-icon.svg">
    </div>
    <div @click="tabSwitch('threads')" title='Threads' class='cursor-pointer'>
      <img v-if="currentTab('threads')" class="tab-label" src="../assets/images/thread-selected.svg">
      <img v-else class="tab-label" src="../assets/images/thread-icon.svg">
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
